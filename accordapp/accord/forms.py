from django.forms import ModelForm
from .models import *
from django.contrib.auth.forms import UserCreationForm


class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'name', 'password1', 'password2']


class LobbyForm(ModelForm):
    class Meta:
        model = Lobby
        fields = '__all__'
        exclude = ['host', 'participants']


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['avatar', 'username', 'email', 'name', 'bio']


class OrderForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)

        try:
            # client_id = UserExtend.objects.values_list('client_id', flat=True).get(user=user)
            self.fields['product'].label_from_instance = self.product_label

        except :
            ### there is not userextend corresponding to this user, do what you want
            print('Hoenai')
            pass
    class Meta:
        model = Order
        fields = ['product', 'customer_name', 'customer_contactnumber', 'customer_address', 'quantity', 'total_price']

    @staticmethod
    def product_label(self):
        return str(self.product_id)


class ProductForm(ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
        exclude=['created_by', 'created_date']
