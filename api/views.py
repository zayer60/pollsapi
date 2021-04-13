from django.shortcuts import render
from rest_framework import generics, status
from .serializers import *
from .models import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import viewsets
from django.contrib.auth import authenticate
from rest_framework.exceptions import PermissionDenied

class PollViewSet(viewsets.ModelViewSet):
    queryset = Poll.objects.all()
    serializer_class = PollSerializer

    def destroy(self, request, *args, **kwargs):
        poll = Poll.objects.get(pk=self.kwargs["pk"])

        if not request.user == poll.created_by:
            raise PermissionDenied("You can not delete this poll.")
        return super().destroy(request, *args, **kwargs)

# class PollListAPI(generics.ListCreateAPIView):
#    queryset = Poll.objects.all()
#    serializer_class = PollSerializer

# class PollDetailsAPI(generics.RetrieveUpdateDestroyAPIView):
#    queryset = Poll.objects.all()
#    serializer_class = PollSerializer


class ChoiceListAPI(generics.ListCreateAPIView):
    serializer_class = ChoiceSerializer

    def get_queryset(self, **kwargs):
        queryset = Choice.objects.filter(poll_id=self.kwargs['pk'])
        return queryset

    def post(self, request, *args, **kwargs):
        poll = Poll.objects.get(pk=self.kwargs["pk"])

        if not request.user == poll.created_by:
            raise PermissionDenied("You can not create choice for this poll.")
        return super().post(request, *args, **kwargs)


class CreateVote(APIView):
    serializer_class = VoteSerializer

    def post(self, request, pk, choice_pk):
        voted_by = request.data.get("voted_by")

        data = {'choice': choice_pk, 'poll': pk, 'voted_by': voted_by}
        serializer = VoteSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CreateUser(generics.CreateAPIView):
    authentication_classes = ()  # exempt from global auth.
    permission_classes = ()  # exempt from global permissiong
    serializer_class = UserSerializer

class LoginView(APIView):
    permission_classes = ()

    def post(self,request):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(username = username, password = password)
        if user:
            return Response({"token":user.auth_token.key})
        else:
            return Response({"error": "Wrong Credentials"}, status=status.HTTP_400_BAD_REQUEST)



# class CreateVote(generics.CreateAPIView):
#    serializer_class = VoteSerializer
