import os
import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime

def fetch_data_from_url(url):
    response = requests.get(url)
    
    if response.status_code != 200:
        print("Erro ao acessar o site")
        return None

    html_content = response.text
    soup = BeautifulSoup(html_content, 'html.parser')

    titles = [title.text.strip() for title in soup.find_all('h1')]
    paragraphs = [p.text.strip() for p in soup.find_all('p')]

    max_length = max(len(titles), len(paragraphs))
    titles += [''] * (max_length - len(titles))
    paragraphs += [''] * (max_length - len(paragraphs))

    data = {
        'Titles': titles,
        'Paragraphs': paragraphs
    }
    df = pd.DataFrame(data)
    
    return df

def generate_report(data_frame):
    report_lines = []
    current_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    report_lines.append(f"Relatório Gerado em: {current_date}\n")
    report_lines.append("Informações Extraídas:\n")
    
    for index, row in data_frame.iterrows():
        title = row['Titles']
        paragraph = row['Paragraphs']
        
        if title:
            report_lines.append(f"Título: {title}\n")
        if paragraph:
            report_lines.append(f"Parágrafo: {paragraph}\n")
        report_lines.append("\n")
    
    return "\n".join(report_lines)

def save_report(report_content, file_path):
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(report_content)
    print(f"Relatório salvo em '{file_path}'")

def main():
    file_path_csv = 'extracted_data.csv'
    file_path_txt = 'report.txt'
    
    while True:
        url = input("Cole a URL do site: ")
        data_frame = fetch_data_from_url(url)

        if data_frame is not None:
            print(data_frame)
            data_frame.to_csv(file_path_csv, index=False)
            print(f"Dados salvos em '{file_path_csv}'")
            
            report_content = generate_report(data_frame)
            save_report(report_content, file_path_txt)

        nova_varredura = input("Deseja fazer uma nova varredura? (S/N): ").strip().upper()
        if nova_varredura == 'S':
            if os.path.exists(file_path_csv):
                os.remove(file_path_csv)
                print(f"Arquivo '{file_path_csv}' foi apagado.")
            if os.path.exists(file_path_txt):
                os.remove(file_path_txt)
                print(f"Arquivo '{file_path_txt}' foi apagado.")
        else:
            continuar_programa = input("Deseja continuar no programa? (S/N): ").strip().upper()
            if continuar_programa == 'N':
                break

if __name__ == "__main__":
    main()


    