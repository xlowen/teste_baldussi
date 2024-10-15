from django.shortcuts import render
from django.http import JsonResponse
import requests

from .models import UserProfile, UserInformation


def get_users_by_gender(request, gender):
    GENEROS_VALIDOS = ['male', 'female', 'homem', 'mulher']
    gender = gender.lower()

    # validação do gênero.

    if gender not in GENEROS_VALIDOS:
        data = {'Erro': f'Acesso incorreto da api com /usuarios/genero/\
                {gender}/. Use homem, mulher, male ou female.'}
        return JsonResponse(data, safe=False)

    match gender:
        case "homem":
            gender = "male"
        case "mulher":
            gender = "female"

        # Usando a ORM do Django pego as informações apenas iguais ao genero
        # que será designado na URL
    users = UserInformation.objects.filter(
        user_profile__gender=gender).select_related('user_profile', 'location')

    # Converte os dados em um dicionario python pra poder converter
    # em JSON usando JsonResponse
    data = [user.as_dict() for user in users]

    if not data:
        return JsonResponse({'Erro': 'Nao há usuarios com estes parametros. \
                             '}, safe=False)
    # Retorna os dados em formato JSON para quem acessa a url
    return JsonResponse(data, safe=False)


def get_users_by_age(request, age):
    if not age:
        data = {'Erro': f'Acesso incorreto da api com /usuarios/idade/{age}/.\
            necessario utilizar um numero inteiro maior que 0.'}
        return JsonResponse(data, safe=False, status=400)

    users = UserInformation.objects.filter(age=age).select_related(
        'user_profile', 'location')
    data = [user.as_dict() for user in users]

    if not data:
        data = {'Inexistente': f'Nao existe usuario com a idade: {age}.'}
        return JsonResponse(data, safe=False, status=404)

    return JsonResponse(data, safe=False, status=200)


# A rest API do django só permite post requests que venham com um CSRF_token
# por questões de segurança. uem acessar essa api via post precisará enviar
# um csrf_token junto aos headers do post request
# Para testar o request criei um form em html que envia os parâmetros
# determinados na especificação do teste.

def post_male_users_age_30(request):
    if request.method == 'POST':
        gender = request.POST.get('genero')
        age = request.POST.get('idade')

        # validação do request body
        gender = gender.lower()
        GENEROS_VALIDOS = ['male', 'female', 'homem', 'mulher']

        match gender:
            case "homem":
                gender = "male"
            case "mulher":
                gender = "female"

        if not gender or not age:
            data = {'Erro': f"Acesso incorreto da api com request body vazio \
                -> 'genero':{gender}?'idade':{age}?'"}

        elif gender not in GENEROS_VALIDOS:
            data = {'Erro': f"Acesso incorreto da api com request body  \
                '{gender}/{age}'. Use homem, mulher, male ou female, e um \
                numero para idade."}

        else:
            # método filter() para definir a query
            # por genero e idade (gender, age)
            users = UserInformation.objects.filter(
                user_profile__gender=gender, age=age).select_related(
                    'user_profile', 'location')
            data = [user.as_dict() for user in users]
            if not data:
                data = {'Erro': f"Nenhum usuario encontrado com estes \
                    parametros -> 'genero':'{gender}', 'idade':'{age}'"}

        return JsonResponse(data, safe=False)
    else:
        return render(request, 'post_teste.html')


def docs(request):
    return render(request, 'docs.html')


def principal(request):
    return render(request, 'home.html')


def listar_todos(request):
    # Selecionar todos os objetos armazenados no modelo UserInformation, 
    # incluindo user e location
    todos_objetos = UserInformation.objects.select_related(
        'user_profile', 'location').all()

    context = {'usuarios': [user.as_dict() for user in todos_objetos]}

    return render(request, 'lista_todos.html', context)


# Criar uma view baseada em função que envia um request
# quando é acessada a rota localhost:8000/povoardb
def fetch_api_users(request):
    BASE_URL = "https://randomuser.me/api/"

    # usar os parâmetros de query da própria api para retornar 100 resultados
    response = requests.get(BASE_URL + "?results=100")

    if response.status_code == 200:        
        # converte o json recebido da api em um dict
        data = response.json()

        # povoa o banco de dados com os dados recebidos acessando os modelos
        for result in data['results']:

            # como e-mail está marcado como unique no modelo, e id é not null,
            # estou pulando inserções no DB que: id seja null(None)
            if result['id']['value'] is None:
                print('Pulando objeto: id_number é nulo')
                continue

            # pulando inserções que conflite com algum ID o e-mail
            # já existente.
            if UserInformation.objects.filter(
                id_number=result['id']['value']) or UserProfile.objects.filter(
                    email=result['email']).exists():

                print('E-mail ou ID conflitantes')

            # Deixei comentado pois só utilizei o código para povoar o BD

            # Se a validação passar, insere os dados no DB
            # else:
            #     user = UserProfile(
            #     gender=result['gender'],
            #     title=result['name']['title'],
            #     first_name=result['name']['first'],
            #     last_name=result['name']['last'],
            #     email=result['email']
            #     )
            #     user.save()

            #     location = Location(
            #         street_number=result['location']['street']['number'],
            #         street_name=result['location']['street']['name'],
            #         city=result['location']['city'],
            #         state=result['location']['state'],
            #         country=result['location']['country'],
            #         postcode=result['location']['postcode'],
            #         latitude=result['location']['coordinates']['latitude'],
            #         longitude=result['location']['coordinates']['longitude'],

            #     )
            #     location.save()

            #     user_info = UserInformation(
            #         user=user,  #relação um pra um com usuario
            #         location=location,  # relação um pra um com o endereco
            #         phone=result['phone'],
            #         cell=result['cell'], # coloquei opcional no banco celular
            #         age=result['dob']['age'],
            #         id_number=result['id']['value'],
            #         picture_large=result['picture']['large'],
            #         picture_medium=result['picture']['medium'],
            #         picture_thumbnail=result['picture']['thumbnail'],
            #         nat=result['nat'],
            #     )
            #     user_info.save()
            context = {'data': data}

    else:
        context = {'erro': 'Houve um erro - Status http:' +
                   response.status_code}

    return render(request, 'index.html', context)
