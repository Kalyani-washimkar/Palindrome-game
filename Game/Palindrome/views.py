from rest_framework import status
from rest_framework.response import Response
from .models import User, Game
from .serializers import UserSerializer, GameSerializer
from django.http import Http404
from django.contrib.auth import authenticate, login, logout
import uuid
import random
from rest_framework.decorators import api_view


# This function is used to perform user CRUD operation.

@api_view(['GET', 'POST', 'PUT', 'DELETE'])
def crud_user(request):
    if request.method == 'GET':
        all_users = User.objects.all()
        serializer = UserSerializer(all_users, many=True)
        return Response(serializer.data, status.HTTP_200_OK)
    
    if request.method == 'POST':
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status.HTTP_201_CREATED)
        return Response(serializer.errors)
    
    if request.method == 'PUT':
        id = request.data.get('id')
        user = User.objects.get(pk=id)
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status.HTTP_200_OK)
        return Response(serializer.errors)
    
    if request.method == 'DELETE':
        id = request.data.get('id')
        user = User.objects.get(pk=id)
        user.delete()
        return Response({'msg':'user is deleted'})


# This function is used for user login.

@api_view()    
def user_login(request):
    data = request.data
    user = authenticate(username=data['username'], password=data['password'])
    if user is not None:
        login(request, user)
        return Response({'msg':'Welcome {}, you are successfully logged into Game!'.format(data['username'])})
    return Response({'error':'Invalid credentials'}, status.HTTP_404_NOT_FOUND)


# This function is used for user logout.

@api_view()
def user_logout(request):
    logout(request)
    return Response({'message':'You are successfully logged out from Game!'})


# This function is used to get the board.

@api_view()
def get_board(request):
    if request.user.is_authenticated:
        existing_game = Game.objects.filter(user=request.user, is_completed=False).first()
        if existing_game:
            existing_game.is_palindrome = False
        else:
            existing_game = Game(user=request.user,
                                game_id=str(uuid.uuid4()),
                                board='',
                                is_completed=False,
                                is_palindrome=False)
            existing_game.save()
        serializer = GameSerializer(existing_game)
        return Response({'Game ID':serializer.data['game_id']})
    return Response({'error':'You need to login first.'})

def get_random_character():
    characters = list('abcdefghijklmnopqrstuvwxyz')
    random.shuffle(characters)
    return random.choice(characters)


# This function is used to update the board.

@api_view()
def update_board(request):
    if request.user.is_authenticated:
        if Game.objects.filter(user=request.user, is_completed=False).exists():
            game = Game.objects.filter(user=request.user, is_completed=False).first()
        else:
            return Response({'message':'Please create a new game by using get-board'})

        if len(game.board) == 6:
            board = game.board
            if board == board[::-1]:
                game.is_completed = True
                game.is_palindrome = True
                game.save()
                return Response({'Congratulations':'Your board string is Palindrome. You Won!'})
            else:
                game.is_completed = True
                game.is_palindrome = False
                game.save()
                return Response({'Game Over':'Your board string is not Palindrome. You Lose!'})
        else:
            game.board += get_random_character()
            game.save()
            return Response({'Game ID': game.game_id, 'Board':game.board})
    return Response({'error':'You need to login first.'})


# This function is used to get list of Game IDs.

@api_view()
def game_id_list(request):
    if request.user.is_authenticated:
        games = Game.objects.filter().values('game_id')
        return Response(games)
    return Response({'error':'You need to login first.'})
    