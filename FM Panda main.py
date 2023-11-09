import pandas as pd
import glob
import os
import tkinter as tk
from tkinter import filedialog

# Tkinter GUI setup
def browse_source_folder():
    folder_path = filedialog.askdirectory()
    source_folder_var.set(folder_path)

def process_and_generate_html_from_gui():
    source_folder = source_folder_var.get()
    process_and_generate_html(source_folder)
    root.quit()  # Add this line to close the Tkinter window after processing

# Create Tkinter window
root = tk.Tk()
root.title("HTML Processing App")

# Tkinter variables
source_folder_var = tk.StringVar()

# Widgets
tk.Label(root, text="Source HTML Folder:").pack(pady=10)
source_folder_entry = tk.Entry(root, textvariable=source_folder_var, width=40)
source_folder_entry.pack(pady=5)
browse_button = tk.Button(root, text="Browse", command=browse_source_folder)
browse_button.pack(pady=5)

process_button = tk.Button(root, text="Process HTML", command=process_and_generate_html_from_gui)
process_button.pack(pady=20)

# End of Tkinter GUI setup

def process_and_generate_html(source_folder):
    # finds most recent file in specified folder
    list_of_files = glob.glob(os.path.join(source_folder, '*.html'))
    if not list_of_files:
        print("No HTML files found in the selected folder.")
        return
    
    latest_file = max(list_of_files, key=os.path.getctime)
    print("Latest HTML file:", latest_file)

    # Read HTML file exported by FM - in this case an example of an output from the squad page
    # This reads as a list, not a dataframe
    squad_rawdata_list = pd.read_html(latest_file, header=0, encoding="utf-8", keep_default_na=False)

    # turn the list into a dataframe
    squad_rawdata = squad_rawdata_list[0]

    # Calculate simple speed and workrate scores
    squad_rawdata['Spd'] = ( squad_rawdata['Pac'] + squad_rawdata['Acc'] ) / 2
    squad_rawdata['Work'] = ( squad_rawdata['Wor'] + squad_rawdata['Sta'] ) / 2
    squad_rawdata['SetP'] = ( squad_rawdata['Jum'] + squad_rawdata['Bra'] ) / 2

    # calculates gk score
    squad_rawdata['gk_essential'] = (
        ( squad_rawdata['Agi'] + 
        squad_rawdata['Ref']) * 5)
    squad_rawdata['gk_core'] = (
        ( squad_rawdata['1v1'] + 
        squad_rawdata['Ant'] + 
        squad_rawdata['Cmd'] + 
        squad_rawdata['Cnt'] + 
        squad_rawdata['Kic'] + 
        squad_rawdata['Pos']) * 3)
    squad_rawdata['gk_secondary'] = (
        ( squad_rawdata['Acc'] +
        squad_rawdata['Aer'] +
        squad_rawdata['Cmp'] + 
        squad_rawdata['Dec'] + 
        squad_rawdata['Fir'] + 
        squad_rawdata['Han'] + 
        squad_rawdata['Pas'] + 
        squad_rawdata['Thr'] + 
        squad_rawdata['Vis']) * 1)
    squad_rawdata['gk'] = ( ((squad_rawdata['gk_essential']) + (squad_rawdata['gk_core']) + (squad_rawdata['gk_secondary'])) / 37 )
    squad_rawdata.gk= squad_rawdata.gk.round(1)
    # for others: squad_rawdata['gk_core'] = ( squad_rawdata[''] + squad_rawdata[''] + squad_rawdata['']+ squad_rawdata['']+ squad_rawdata['']+ squad_rawdata['']+ squad_rawdata['']) / 2

    # calculates fb score
    squad_rawdata['fb_essential'] = ( 
        squad_rawdata['Wor'] +
        squad_rawdata['Acc'] + 
        squad_rawdata['Pac'] + 
        squad_rawdata['Sta'])
    squad_rawdata['fb_core'] = ( 
        squad_rawdata['Cro'] + 
        squad_rawdata['Dri'] + 
        squad_rawdata['Mar'] + 
        squad_rawdata['OtB'] + 
        squad_rawdata['Tck'] + 
        squad_rawdata['Tea'])
    squad_rawdata['fb_secondary'] = ( 
        squad_rawdata['Agi'] + 
        squad_rawdata['Ant'] + 
        squad_rawdata['Cnt'] + 
        squad_rawdata['Dec'] + 
        squad_rawdata['Fir'] + 
        squad_rawdata['Pas'] + 
        squad_rawdata['Pos'] + 
        squad_rawdata['Tec'])
    squad_rawdata['fb'] =( ( ( squad_rawdata['fb_essential'] * 5) + ( squad_rawdata['fb_core'] * 3) + (squad_rawdata['fb_secondary'] * 1)) / 46 )
    squad_rawdata.fb= squad_rawdata.fb.round(1)

    # calculates cb score
    squad_rawdata['cb_core'] = ( squad_rawdata['Cmp'] + squad_rawdata['Hea'] + squad_rawdata['Jum']+ squad_rawdata['Mar']+ squad_rawdata['Pas']+ squad_rawdata['Pos']+ squad_rawdata['Str'] + squad_rawdata['Tck'] + squad_rawdata['Pac']) / 9
    squad_rawdata['cb_secondary'] = ( squad_rawdata['Agg'] + squad_rawdata['Ant'] + squad_rawdata['Bra']+ squad_rawdata['Cnt']+ squad_rawdata['Dec']+ squad_rawdata['Fir']+ squad_rawdata['Tec']+ squad_rawdata['Vis']) / 8
    squad_rawdata['cb'] =( ( squad_rawdata['cb_core'] * 0.75) + (squad_rawdata['cb_secondary'] * 0.25))
    squad_rawdata.cb= squad_rawdata.cb.round(1)

    # calculates dm score
    squad_rawdata['dm'] = ((
        ( squad_rawdata['Wor'] * 5) + 
        ( squad_rawdata['Pac'] * 5) + 
        ( squad_rawdata['Sta'] * 3) + 
        ( squad_rawdata['Pas'] * 3) + 
        ( squad_rawdata['Tck'] * 2) + 
        ( squad_rawdata['Ant'] * 2) + 
        ( squad_rawdata['Cnt'] * 2) + 
        ( squad_rawdata['Pos'] * 2) + 
        ( squad_rawdata['Bal'] * 2) + 
        ( squad_rawdata['Agi'] * 2) + 
        ( squad_rawdata['Tea'] * 1) + 
        ( squad_rawdata['Fir'] * 1) +
        ( squad_rawdata['Mar'] * 1) +
        ( squad_rawdata['Agg'] * 1) +
        ( squad_rawdata['Cmp'] * 1) +
        ( squad_rawdata['Dec'] * 1) +
        ( squad_rawdata['Str'] * 1) ) / 35)
    squad_rawdata.dm= squad_rawdata.dm.round(1)

    # calculates segundo volante on attack score
    squad_rawdata['vol'] = ((
        ( squad_rawdata['Wor'] * 5) + 
        ( squad_rawdata['Pac'] * 5) + 
        ( squad_rawdata['Sta'] * 3) + 
        ( squad_rawdata['Pas'] * 3) + 
        ( squad_rawdata['Tck'] * 2) + 
        ( squad_rawdata['Ant'] * 2) + 
        ( squad_rawdata['Cnt'] * 2) + 
        ( squad_rawdata['Pos'] * 2) + 
        ( squad_rawdata['Tea'] * 2) + 
        ( squad_rawdata['Fir'] * 1) +
        ( squad_rawdata['Mar'] * 1) +
        ( squad_rawdata['Agg'] * 1) +
        ( squad_rawdata['Cmp'] * 1) +
        ( squad_rawdata['Dec'] * 1) +
        ( squad_rawdata['Str'] * 1) ) / 32)
    squad_rawdata.vol= squad_rawdata.vol.round(1)

    # calculates box2box score
    squad_rawdata['box2'] = (
        ( squad_rawdata['Pas'] * 5) + 
        ( squad_rawdata['Wor'] * 5) + 
        ( squad_rawdata['Sta'] * 4) + 
        ( squad_rawdata['Tck'] * 3) + 
        ( squad_rawdata['OtB'] * 3) + 
        ( squad_rawdata['Tea'] * 3) + 
        ( squad_rawdata['Vis'] * 2) + 
        ( squad_rawdata['Str'] * 2) + 
        ( squad_rawdata['Dec'] * 2) + 
        ( squad_rawdata['Pos'] * 2) + 
        ( squad_rawdata['Pac'] * 2) +
        ( squad_rawdata['Agg'] * 1) +
        ( squad_rawdata['Ant'] * 1) +
        ( squad_rawdata['Fin'] * 1) +
        ( squad_rawdata['Lon'] * 1) +
        ( squad_rawdata['Cmp'] * 1) +
        ( squad_rawdata['Acc'] * 1) +
        ( squad_rawdata['Bal'] * 1) +
        ( squad_rawdata['Fir'] * 1) +
        ( squad_rawdata['Dri'] * 1) +
        ( squad_rawdata['Tec'] * 1))
    squad_rawdata.box2= squad_rawdata.box2.round(0)

    # calculates winger score
    squad_rawdata['w_core'] = ( squad_rawdata['Acc'] + squad_rawdata['Cro'] + squad_rawdata['Dri']+ squad_rawdata['OtB']+ squad_rawdata['Pac']+ squad_rawdata['Tec']) / 6
    squad_rawdata['w_secondary'] = ( squad_rawdata['Agi'] + squad_rawdata['Fir'] + squad_rawdata['Pas']+ squad_rawdata['Sta']+ squad_rawdata['Wor']) / 5
    squad_rawdata['w'] =( ( squad_rawdata['w_core'] * 0.75) + (squad_rawdata['w_secondary'] * 0.25))
    squad_rawdata.w= squad_rawdata.w.round(1)

    # calculates inverted winger score 
    squad_rawdata['amrl'] = ((
        ( squad_rawdata['Acc'] * 5) + 
        ( squad_rawdata['Pac'] * 5) + 
        ( squad_rawdata['Wor'] * 5) + 
        ( squad_rawdata['Dri'] * 3) + 
        ( squad_rawdata['Pas'] * 3) + 
        ( squad_rawdata['Tec'] * 3) + 
        ( squad_rawdata['OtB'] * 3) +
        ( squad_rawdata['Cro'] * 1) + 
        ( squad_rawdata['Fir'] * 1) +
        ( squad_rawdata['Cmp'] * 1) +
        ( squad_rawdata['Dec'] * 1) +
        ( squad_rawdata['Vis'] * 1) +
        ( squad_rawdata['Agi'] * 1) + 
        ( squad_rawdata['Sta'] * 1))/ 34)
    squad_rawdata.amrl= squad_rawdata.amrl.round(1)

    # calculates amc score
    squad_rawdata['amc'] = (
        ( squad_rawdata['Vis'] * 4) + 
        ( squad_rawdata['OtB'] * 4) + 
        ( squad_rawdata['Pas'] * 4) + 
        ( squad_rawdata['Dec'] * 3) + 
        ( squad_rawdata['Ant'] * 3) + 
        ( squad_rawdata['Cmp'] * 3) + 
        ( squad_rawdata['Tec'] * 3) + 
        ( squad_rawdata['Dri'] * 1) + 
        ( squad_rawdata['Fir'] * 1) + 
        ( squad_rawdata['Fla'] * 1) + 
        ( squad_rawdata['Lon'] * 1) + 
        ( squad_rawdata['Agi'] * 1) + 
        ( squad_rawdata['Fin'] * 1))
    squad_rawdata.amc= squad_rawdata.amc.round(0)

    # calculates striker score
    squad_rawdata['str_core'] = ( squad_rawdata['Cmp'] + squad_rawdata['Fin'] + squad_rawdata['OtB'] + squad_rawdata['Pac']) / 4
    squad_rawdata['str_secondary'] = ( squad_rawdata['Acc'] + squad_rawdata['Agi'] + squad_rawdata['Ant']+ squad_rawdata['Bal']+ squad_rawdata['Dec']+ squad_rawdata['Dri']+ squad_rawdata['Fir']+ squad_rawdata['Pas']+ squad_rawdata['Sta']+ squad_rawdata['Tec']+ squad_rawdata['Wor']) / 11
    squad_rawdata['str'] =( ( squad_rawdata['str_core'] * 0.5) + (squad_rawdata['str_secondary'] * 0.5))
    squad_rawdata.str= squad_rawdata.str.round(1)

    # builds squad dataframe using only columns that will be exported to HTML
    try:
        
        squad = squad_rawdata[['Inf','Name','Age','Club','Transfer Value','Wage','Nat','Position','Personality','Media Handling','Left Foot', 'Right Foot','Spd','Jum','Str','Work','Height','gk','fb','cb','vol','str']]
    except KeyError:
        squad = squad_rawdata[['Inf','Name','Age','Club','Transfer Value','Nat','Position','Personality','Media Handling','Left Foot', 'Right Foot','Spd','Jum','Str','Work','Height','gk','fb','cb','vol','str']]

    # taken from here: https://www.thepythoncode.com/article/convert-pandas-dataframe-to-html-table-python
    # creates a function to make a sortable html export

    def generate_html(dataframe: pd.DataFrame):
        # get the table HTML from the dataframe
        table_html = dataframe.to_html(table_id="table", index=False)
        # construct the complete HTML with jQuery Data tables
        # You can disable paging or enable y scrolling on lines 20 and 21 respectively
        html = f"""
        <html>
        <header>
            <link href="https://cdn.datatables.net/1.11.5/css/jquery.dataTables.min.css" rel="stylesheet">
        </header>
        <body>
        {table_html}
        <script src="https://code.jquery.com/jquery-3.6.0.slim.min.js" integrity="sha256-u7e5khyithlIdTpu22PHhENmPcRdFiHRjhAuHcs05RI=" crossorigin="anonymous"></script>
        <script type="text/javascript" src="https://cdn.datatables.net/1.11.5/js/jquery.dataTables.min.js"></script>
        <script>
            $(document).ready( function () {{
                $('#table').DataTable({{
                    paging: false,
                    order: [[12, 'desc']],
                    // scrollY: 400,
                }});
            }});
        </script>
        </body>
        </html>
        """
        # return the html
        return html

    # generates random file name for write-out of html file
    import uuid
    filename = str(uuid.uuid4()) + ".html"
    filename

    # creates a sortable html export from the dataframe 'squad'

    html = generate_html(squad)
    

    

    output_directory = os.path.join(os.path.expanduser("~"), "Desktop", "FM Panda scout files")
    output_filepath = os.path.join(os.path.expanduser("~"), "Desktop", "FM Panda scout files", filename)
    os.makedirs(output_directory, exist_ok=True)  # Create the directory if it doesn't exist

    # Write the HTML content to the file
    open(output_filepath, "w", encoding="utf-8").write(html)

    print("HTML file saved to:", output_filepath)
root.mainloop()