import codecs
import csv
import subprocess
import sys
import pandas as pd
import tempfile  # Import the tempfile module

def process_files(file1, file2):
    # Check if both files have .csv extension
    if not (file1.lower().endswith(".csv") and file2.lower().endswith(".csv")):
        print("Both files must be in CSV format.")
        return    
    return file1, file2



def write_dataframes_to_csv(coincidences,df1, df2):
    # Crear un archivo CSV temporal
    with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False, encoding='utf-8') as temp_file:
        # Escribir df1 en el archivo CSV
        temp_file.write("DF1 (Unique):\n")
        temp_file.write(df1.to_csv(index=False, encoding='utf-8'))
        temp_file.write("\n\n")
        
        # Escribir df2 en el archivo CSV
        temp_file.write("DF2 (Unique):\n")
        temp_file.write(df2.to_csv(index=False, encoding='utf-8'))
        temp_file.write("\n")

        temp_file.write("Coincidences:\n")
        temp_file.write(coincidences.to_csv(index=False, encoding='utf-8'))
        temp_file.write("\n")


        # Obtener el nombre del archivo temporal
        temp_filename = temp_file.name
        print("Archivo CSV temporal creado en:", temp_filename)

        try:
            subprocess.Popen(['xdg-open', temp_filename])  # Para Linux
        except OSError:
            try:
                subprocess.Popen(['open', temp_filename])  # Para macOS
            except OSError:
                    subprocess.Popen(['start', '', temp_filename], shell=True)  # Para Windows
    
    return temp_filename
    

def compare_and_highlight(file1, file2):
    # Read CSV files into DataFrames
    df1 = pd.read_csv(file1)
    df2 = pd.read_csv(file2)

    common_rows = pd.merge(df1, df2, how='inner')

    unique_to_df1 = pd.merge(df1, df2, how='outer', indicator=True).query("_merge == 'left_only'").drop('_merge', axis=1)
    unique_to_df2 = pd.merge(df1, df2, how='outer', indicator=True).query("_merge == 'right_only'").drop('_merge', axis=1)
    coincidences,df1,df2=find_coincidences(unique_to_df1,unique_to_df2)


    coincidences_df = pd.DataFrame(coincidences, columns=['Phase1', 'Task ID1', 'Task Title1', 'Priority1', 'Description1', 'Completion Status1', 'Tags1', 'Problem ID1', 'Problem Title1', 'Risk Rating1', 'Business Unit1', 'Application1', 'Project1', 'Project Attributes1', 'Issue Tracker Tickets1',
                                                          'Phase2', 'Task ID2', 'Task Title2', 'Priority2', 'Description2', 'Completion Status2', 'Tags2', 'Problem ID2', 'Problem Title2', 'Risk Rating2', 'Business Unit2', 'Application2', 'Project2', 'Project Attributes2', 'Issue Tracker Tickets2'])
    return coincidences_df,df1,df2




def find_coincidences(df1, df2):
    coincidences = []
    for index1, row1 in df1.iterrows():
        found = False
        for index2, row2 in df2.iterrows():
            if (row1['Task ID'] == row2['Task ID'] or
                row1['Task Title'] == row2['Task Title'] or
                row1['Description'] == row2['Description'] or
                row1['Problem ID'] == row2['Problem ID']):
                coincidences.append((row1['Phase'], row1['Task ID'], row1['Task Title'], row1['Priority'], row1['Description'], row1['Completion Status'], row1['Tags'], row1['Problem ID'], row1['Problem Title'], row1['Risk Rating'], row1['Business Unit'], row1['Application'], row1['Project'], row1['Project Attributes'], row1['Issue Tracker Tickets'], 
                                     row2['Phase'], row2['Task ID'], row2['Task Title'], row2['Priority'], row2['Description'], row2['Completion Status'], row2['Tags'], row2['Problem ID'], row2['Problem Title'], row2['Risk Rating'], row2['Business Unit'], row2['Application'], row2['Project'], row2['Project Attributes'], row2['Issue Tracker Tickets']))
                found = True
                break  # Break to avoid adding the same match multiple times
        if found:
            df1.drop(index1, inplace=True)  # Eliminate the row from df1
            df2.drop(index2, inplace=True)  # Eliminate the row from df2
    return coincidences, df1, df2



def main():
    if len(sys.argv) != 3:
        print("Please drag and drop exactly two files onto this script.")
        return

    file1, file2 = sys.argv[1], sys.argv[2]
    file1,file2 = process_files(file1, file2)
    coincidences,df1,df2=compare_and_highlight(file1,file2)
    write_dataframes_to_csv(coincidences,df1,df2)


if __name__ == "__main__":
    main()

