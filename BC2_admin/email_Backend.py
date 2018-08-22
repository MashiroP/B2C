from user.models import profile
from django.contrib.auth.hashers import make_password, check_password
class EmailBackend(object):
    
    def clik_password(self,password):
        dj_ps=make_password(password.password, None, 'pbkdf2_sha256')
        ps_bool = check_password(password.password, dj_ps)
        return ps_bool
    def authenticate(self, request, **credentials):
        # 要注意登录表单中用户输入的用户名或者邮箱的 field 名均为 username
        email = credentials.get('email', credentials.get('username'))
        try:
            user = profile.objects.get(email=email)
        except profile.DoesNotExist:
            pass
        else:
            
            dj_ps = make_password(user.password, None, 'pbkdf2_sha256')
    
            ps_bool = check_password(user.password, dj_ps)
            if check_password((credentials["password"])):
                return user
            

    def get_user(self, user_id):
        """
        该方法是必须的
        """
        try:
            return profile.objects.get(pk=user_id)
        except profile.DoesNotExist:
            return None
