import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password, check_password
from .models import Player

@csrf_exempt # Вимикаємо CSRF для спрощення запитів від ігрового клієнта
def register(request):
    """Реєстрація нового гравця"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            
            if Player.objects.filter(nick=data['nick']).exists():
                return JsonResponse({'error': 'Гравець з таким ніком вже існує'}, status=400)
            
            # Створюємо гравця, хешуючи пароль
            player = Player(
                nick=data['nick'],
                password=make_password(data['password']),
                position_x=0,  # Початкові координати
                position_y=0
            )
            player.save()
            return JsonResponse({'message': 'Реєстрація успішна'}, status=201)
        
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    
    return JsonResponse({'error': 'Метод не дозволено'}, status=405)

@csrf_exempt
def login(request):
    """Авторизація гравця (вхід у гру)"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            player = Player.objects.filter(nick=data['nick']).first()
            
            # Перевіряємо, чи існує гравець і чи збігається пароль
            if player and check_password(data['password'], player.password):
                player.status = True  # Встановлюємо статус "онлайн"
                player.save()
                return JsonResponse({
                    'message': 'Вхід успішний', 
                    'player_id': player.id,
                    'best_size': player.best_size
                })
                
            return JsonResponse({'error': 'Невірний нік або пароль'}, status=401)
            
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

def return_best_players(request):
    allPlayers = []
    for player in Player.objects.all():
        allPlayers.append( 
            {'nick': player.nick,'best_size': player.best_size}
        )
    return JsonResponse( {'data': allPlayers } )
 
from django.views.generic import ListView
class ListView_best_players(ListView):
    model = Player 
    template_name = 'best_players.html'
    context_object_name = 'players'
    def get_queryset(self):  return Player.objects.all().order_by('-best_size')

@csrf_exempt
def update_state(request, player_id): 
    """Оновлення координат та розміру під час гри"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            player = Player.objects.get(id=player_id)
            
            # Оновлюємо поточні показники
            player.position_x = data.get('position_x', player.position_x)
            player.position_y = data.get('position_y', player.position_y)
            player.size = data.get('size', player.size)
            
            # Оновлюємо найкращий результат, якщо поточний розмір більший
            if player.size > player.best_size:
                player.best_size = player.size
                
            player.save()
            return JsonResponse({'message': 'Стан оновлено'})
            
        except Player.DoesNotExist:
            return JsonResponse({'error': 'Гравця не знайдено'}, status=404)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

@csrf_exempt
def logout(request, player_id):
    """Вихід з гри (офлайн)"""
    if request.method == 'POST':
        try:
            player = Player.objects.get(id=player_id)
            player.status = False  # Встановлюємо статус "офлайн"
            player.save()
            return JsonResponse({'message': 'Успішний вихід'})
        except Player.DoesNotExist:
            return JsonResponse({'error': 'Гравця не знайдено'}, status=404)
        

from django.shortcuts import render

def index(request):
    """Головна сторінка з інтерфейсом"""
    return render(request, 'index.html')


def game_view(request):
    """Сторінка самої гри"""
    return render(request, 'game.html')