import requests
import json

base_url = 'https://www.instagram.com'

class user():
    def __init__(self):
        self.session = requests.Session()
        r = self.session.get(base_url)
        self.session.headers.update({'X-CSRFToken': r.cookies['csrftoken']})

    def login(self, user, password):
        url =('/accounts/login/ajax/')
        codi = ('#PWD_INSTAGRAM_BROWSER:0:0:' + password)

        r = self.session.post(base_url + url, data={'username': user, 'enc_password': codi})
        self.session.headers.update({'X-CSRFToken': r.cookies['csrftoken']})

        #conferir se está logado e enviar informações para usuario
        self.t = json.loads(r.content.decode('utf-8'))

        if self.t['authenticated']:
            print('Autenticado: Sim', '\nUser: ', self.t['userId'], '\nStatus: ', self.t['status'])
        else:
            print('Login Failed')
    
    def unfollow(self, username_target):
        try:
            conn = self.t['authenticated']
        except:
            conn = False

        if conn:
            aux = info_()
            id_user = aux.id_user(username_target)

            url = '/web/friendships/'+ id_user +'/unfollow/'

            r = self.session.post(base_url + url)
            self.session.headers.update({'X-CSRFToken': r.cookies['csrftoken']})

            t = json.loads(r.content.decode('utf-8'))

            if t['status']:
                print('deixou de seguir: ', username_target)
            else:
                print('Não foi possível deixar de seguir')
        else:
            print('Usuario não logado')

    def follow(self, username_target):
        try:
            conn = self.t['authenticated']
        except:
            conn = False

        if conn:
            aux = info_()
            id_user = aux.id_user(username_target)

            url = '/web/friendships/'+ id_user +'/follow/'

            r = self.session.post(base_url + url)
            self.session.headers.update({'X-CSRFToken': r.cookies['csrftoken']})
            
            t = json.loads(r.content.decode('utf-8'))

            if t['status']:
                print('Começou a seguir: ', username_target)
            else:
                print('Não foi possível Seguir')
        else:
            print('Usuario não logado')
    
    def like(self, url_pub, username_target):
        try:
            conn = self.t['authenticated']
        except:
            conn = False

        if conn:
            aux = info_()
            username = aux.id_user(username_target)
            id_pub = aux.id_pub(url_pub, username)

            url = '/web/likes/' + id_pub + '/like/'

            r = self.session.post(base_url + url)
            self.session.headers.update({'X-CSRFToken': r.cookies['csrftoken']})
            
            t = json.loads(r.content.decode('utf-8'))

            if t['status']:
                print('Curtiu a publicação do usuário ', username_target)
            else:
                print('Não foi possível curtir a publicação')
        else:
            print('Usuario não logado')
    
    def unlike(self, url_pub, username_target):
        try:
            conn = self.t['authenticated']
        except:
            conn = False

        if conn:
            aux = info_()
            username = aux.id_user(username_target)
            id_pub = aux.id_pub(url_pub, username)

            url = '/web/likes/' + id_pub + '/unlike/'

            r = self.session.post(base_url + url)
            self.session.headers.update({'X-CSRFToken': r.cookies['csrftoken']})
            
            t = json.loads(r.content.decode('utf-8'))

            if t['status']:
                print('Descurtiu a publicação do usuário ', username_target)
            else:
                print('Não foi possível Descurtir a publicação')
        else:
            print('Usuario não logado')
    
    def comment(self, url_pub, username_target, comment, replied_to_comment_id = ""):
        try:
            conn = self.t['authenticated']
        except:
            conn = False

        if conn:
            aux = info_()
            username = aux.id_user(username_target)
            id_pub = aux.id_pub(url_pub, username)

            url = '/web/comments/'+ id_pub +'/add/'

            r = self.session.post(base_url + url, data={'comment_text': comment, 'replied_to_comment_id': replied_to_comment_id})
            self.session.headers.update({'X-CSRFToken': r.cookies['csrftoken']})

            self.t = json.loads(r.content.decode('utf-8'))

            if self.t['status'] == 'ok':
                print('Comentado com sucesso!')
            else:
                print('Não foi possível comentar!')
        else:
            print ('Usuário não logado!!')
        
    def logout(self):
        try:
            conn = self.t['authenticated']
        except:
            conn = False

        if conn:
            userid = self.t['userId']
            url = '/accounts/logout/ajax/'

            self.session.post(base_url + url, data={'one_tap_app_login': '0', 'user_id': userid})
            
            print('Usuário deslogado com sucesso!')
            
        else:
            print('Nenhum usuário logado')





class info_():
    def id_pub(self, url_pub, id_user):
        base_url = 'https://api.instagram.com/oembed/?url='

        session = requests.Session()
        r = session.get(base_url + url_pub)

        t = json.loads(r.content.decode('utf-8'))

        mix = str(t['media_id'])

        id_us = '_' + id_user

        mix = mix.replace(id_us,'')
        
        return mix
    
    def id_user(self, profile_user):
        url = 'https://www.instagram.com/'+ profile_user +'/?__a=1'

        session = requests.Session()
        r = session.get(url)

        t = json.loads(r.content.decode('utf-8'))
        
        t = t['graphql']['user']['id']

        return t