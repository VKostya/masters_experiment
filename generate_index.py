import os

results_dir = 'results'
index_file_path = os.path.join(results_dir, 'index.html')


def generate_html_index(results_directory):
    txt_files = [f for f in os.listdir(results_directory) if f.endswith('.txt')]
    
    html_content = '<html>\n<head>\n<title>Test Results</title>\n</head>\n<body>\n'
    html_content += '<h1>Test Results</h1>\n<ul>\n'
    
    for txt_file in txt_files:
        file_path = os.path.join(results_directory, txt_file)
        link = f'https://vkostya.github.io/masters_experiment/{file_path}'
        html_content += f'<li><a href="{link}">{txt_file}</a></li>\n'
    
    html_content += '</ul>\n</body>\n</html>'

    with open(index_file_path, 'w') as index_file:
        index_file.write(html_content)
    print(f'Index file created at {index_file_path}')

generate_html_index(results_dir)
