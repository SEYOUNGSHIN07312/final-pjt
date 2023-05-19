from rest_framework.response import Response
from django.shortcuts import render, get_list_or_404, get_object_or_404
import requests
import json
from rest_framework.decorators import api_view
from rest_framework import status
from .models import *
from .serializers import *
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth import get_user_model

TMDB_API_KEY = '386ea6e619bc3b5721f33392e34505c2'

# Create your views here.
def get_top_rated(request):
    total_data = []
    
    for i in range(1, 501):
        request_url = f'https://api.themoviedb.org/3/movie/top_rated?api_key={TMDB_API_KEY}&language=ko-KR&page={i}'
        movies = requests.get(request_url).json()

        for movie in movies['results']:
            if movie.get('release_date', '') and movie.get('title', '') and movie.get('overview', '') and movie.get('poster_path', ''):
                fields = {
                    'id': movie['id'],
                    'title': movie['title'],
                    'original_title': movie['original_title'],
                    'overview': movie['overview'],
                    'release_date': movie['release_date'],
                    'popularity': movie['popularity'],
                    'poster_path': movie['poster_path'],
                    'genres': movie['genre_ids'],
                }

                data = {
                    'pk': movie['id'],
                    'model': 'api.movie',
                    'fields': fields
                }

                total_data.append(data)
    
    with open('top_rated_movie_data.json', 'w', encoding='utf-8') as w:
        json.dump(total_data, w, indent=2, ensure_ascii=False)



def get_genres(request):
    total_data = []
    request_url = f'https://api.themoviedb.org/3/genre/movie/list?api_key={TMDB_API_KEY}&language=ko-KR'
    genres = requests.get(request_url).json()

    for genre in genres['genres']:
        fields = {
            'id': genre['id'],
            'name': genre['name'],
        }

        data = {
            'pk': genre['id'],
            'model': 'api.genre',
            'fields': fields
        }

        total_data.append(data)

    with open('genre_data.json', 'w', encoding='utf-8') as w:
        json.dump(total_data, w, indent=2, ensure_ascii=False)


@api_view(['GET'])
def movie_list(request):
    if request.method == 'GET':
        movies = get_list_or_404(Movie)
        serializer = MovieSerializer(movies, many=True)
        return Response(serializer.data)
    
# @api_view(['GET'])
# def movie_detail(request, movie_id):
#     if request.method == 'GET':
#         movie = get_object_or_404(Movie, id=movie_id)
#         serializer = MovieSerializer(movie)
#         return Response(serializer.data)
    
@api_view(['GET'])
def movie_detail(request, movie_id):
    if request.method == 'GET':
        moviedetail = get_object_or_404(Movie, pk=movie_id)

        request_url = f'https://api.themoviedb.org/3/movie/{movie_id}/credits?api_key={TMDB_API_KEY}&language=ko-KR'
        movie = requests.get(request_url).json()
        actors = []
        directors = []
        for person in movie['cast']:
            if person['known_for_department'] == 'Acting':
                actors.append([person['name'], person['popularity']])
            elif person['known_for_department'] == 'Directing':
                directors.append([person['name'], person['popularity']])
        actors.sort(key = lambda x : -x[1])
        directors.sort(key = lambda x : -x[1])

        setattr(moviedetail, 'actors', actors[:4])
        setattr(moviedetail, 'directors', directors[0])

        serializer = MovieDetailSerializer(moviedetail)

        return Response(serializer.data)
    


@api_view(['POST', 'GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def create_review(request, movie_id):
    movie = get_object_or_404(Movie, pk=movie_id)
    if request.method == 'POST':
        serializer = MovieReviewSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(movie=movie, user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    elif request.method == 'GET':
        movieReviews = movie.reviews.all()
        serializer = MovieReviewSerializer(movieReviews, many=True)
        return Response(serializer.data)
    

@api_view(['DELETE', 'PUT'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def review_detail(request, review_id):
    review = get_object_or_404(MovieReview, pk=review_id)
    if request.user.moviereview_set.filter(pk=review_id).exists():
        if request.method == 'DELETE':
            review.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        
        elif request.method == 'PUT':
            serializer = MovieReviewSerializer(review, data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data)
    return Response({'detail': '권한이 없습니다.'})


@api_view(['POST', 'GET'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def article_list(request):
    if request.method == 'GET':
        articles = get_list_or_404(Article)
        serializer = ArticleSerializer(articles, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = ArticleSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        

@api_view(['GET', 'DELETE', 'PUT'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def article_detail(request, article_id):
    article = get_object_or_404(Article, pk=article_id)
    if request.method == 'GET':
        serializer = ArticleDetailSerializer(article)
        return Response(serializer.data)
    
    if request.user.article_set.filter(pk=article_id).exists():
        if request.method == 'DELETE':
            article.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        
        elif request.method == 'PUT':
            serializer = ArticleDetailSerializer(article, data=request.data, partial=True)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(serializer.data)
    return Response({'detail': '권한이 없습니다.'})


@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def create_comment(request, article_id):
    article = get_object_or_404(Article, pk=article_id)
    if request.method == 'POST':
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(article=article, user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['DELETE'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def comment_delete(request, comment_id):
    comment = get_object_or_404(ArticleComment, pk=comment_id)
    if request.method == 'DELETE':
        if request.user.articlecomment_set.filter(pk=comment_id).exists():
            comment.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({'detail': '권한이 없습니다.'})
    

@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def movie_detail_like(request, movie_id):
    if request.method == 'POST':
        movie = get_object_or_404(Movie, pk=movie_id)
        if movie.like_users.filter(pk=request.user.pk).exists():
            movie.like_users.remove(request.user)
            return Response({'detail': '좋아요 취소'})
        else:
            movie.like_users.add(request.user)
            return Response({'detail': '좋아요 완료'})
        


@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def review_detail_like(request, review_id):
    if request.method == 'POST':
        review = get_object_or_404(MovieReview, pk=review_id)
        if review.like_users.filter(pk=request.user.pk).exists():
            review.like_users.remove(request.user)
            return Response({'detail': '좋아요 취소'})
        else:
            review.like_users.add(request.user)
            return Response({'detail': '좋아요 완료'})
        


@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def article_datail_like(request, article_id):
    if request.method == 'POST':
        article = get_object_or_404(Article, pk=article_id)
        if article.like_users.filter(pk=request.user.pk).exists():
            article.like_users.remove(request.user)
            return Response({'detail': '좋아요 취소'})
        else:
            article.like_users.add(request.user)
            return Response({'detail': '좋아요 완료'})