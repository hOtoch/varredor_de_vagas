import PySimpleGUI as sg 
from threading import Thread
from interface.utilities import validate_username,init_scrap
from time import sleep


sg.theme("Purple")

def janela_config():
    uf_estados_brasileiros = ["AC", "AL", "AP", "AM", "BA", "CE", "DF", "ES", "GO", "MA", "MT", "MS", "MG", "PA", "PB", "PR", "PE", "PI", "RJ", "RN", "RS", "RO", "RR", "SC", "SP", "SE", "TO"]

    layout_config = [
        [sg.Text('Scraper de vagas',justification='center',size=(37, 1),font=('Helvetica', 12, 'bold'))],
        [sg.Text('Usuário do Github')],
        [sg.Input(key='user')],
        [sg.Text(key='invalid_user')],
        [sg.Text('Preferências da vaga')],
        [sg.Input(key='description')],
        [sg.Frame('Localização',[
            [sg.Radio('Todos',group_id='localizacao_radio',key='todos_radio',default=True, enable_events=True),
             sg.Radio('Remoto',group_id='localizacao_radio',key='remoto_radio',enable_events=True),
             sg.Radio('Presencial',group_id='localizacao_radio',key='presencial_radio',enable_events=True)],
            [sg.Combo(uf_estados_brasileiros, key='uf'), sg.Text('UF')],
            [sg.Input(key='city',size=(15,1)), sg.Text('Cidade')]
        ])],
        [sg.Text('Selecione o diretório que o arquivo será salvo')],
        [sg.InputText(key='-DIRPATH-'), sg.FolderBrowse()],
        [sg.Button('Salvar diretório')],
        [sg.Text(key='verify_path')],
        [sg.Button('Iniciar',key='start',disabled=True)]
    ]
    
    return sg.Window('Configurações', layout=layout_config, finalize=True)

def janela_inicializacao():
    layout_inicializacao = [
        [sg.Text('Scraper de vagas',justification='center',size=(37, 1),font=('Helvetica', 12, 'bold'))],
        [sg.Output(size=(50,20))],
        [sg.Button('Sair', disabled=True), sg.Text(key='progresso')]
    ]
    
    return sg.Window('Inicialização', layout=layout_inicializacao,finalize=True)

janela_config_, janela_inicializacao_ = janela_config() , None


while True:
    window, event, values = sg.read_all_windows()
    
    if event == sg.WIN_CLOSED:
        break
    
    if window == janela_config_:
        
        if event in ['todos_radio', 'remoto_radio', 'presencial_radio']:
            if values['remoto_radio']:
                window['uf'].update(disabled=True)
                window['city'].update(value='Home Office',disabled=True)
                
            else:
                window['uf'].update(disabled=False)
                window['city'].update(disabled=False)
       
        if event == 'Salvar diretório':  
            # Verifica se o campo de diretório está vazio
            if values['-DIRPATH-'] == '':
                window['verify_path'].update('Diretório inválido',text_color='red')
                window['start'].update(disabled=True)  # Desabilita o botão 'Iniciar'
            else:
                window['verify_path'].update('Diretório válido',text_color='green')
                window['start'].update(disabled=False)  # Habilita o botão 'Iniciar'
            
        elif event == 'start':
            thread_validar_usuario = Thread(target=validate_username, args=(window,values['user']), daemon=True)
            thread_validar_usuario.start()
            
        
        elif event == 'validate_username':
            thread_validar_usuario.join()
            result_validate = values['validate_username']
            
            if result_validate['result'] == True:
                janela_config_.hide()
                if janela_inicializacao_:
                    janela_inicializacao_.un_hide()
                else:
                    janela_inicializacao_ = janela_inicializacao()
                
                janela_inicializacao_.write_event_value('init_bot','Verificando vagas...')
               
                thread_init_scrap = Thread(target=init_scrap, args=(window,values), daemon=True)
                thread_init_scrap.start()
                
            else:
                window['invalid_user'].update(result_validate['message'],text_color='red')
        
        elif event == 'final_bot':
            thread_init_scrap.join()
            janela_inicializacao_.write_event_value('scrapy_finalized','Scraper finalizado!')
                  
            
                
    if window == janela_inicializacao_:
        if event=='Sair':
            break;
        
        elif event == 'init_bot':
            window['progresso'].update(values['init_bot'])
        
        elif event=='scrapy_finalized':
            window['progresso'].update(values['scrapy_finalized'], text_color='green')
            window['Sair'].update(disabled=False)
        
    
        
# Fechando as janelas ao finalizar
if janela_config_:
    janela_config_.close()
if janela_inicializacao_:
    janela_inicializacao_.close() 
    