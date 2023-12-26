from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Person
from .serializers import PersonSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
import logging
from django.core.mail import send_mail

error_logger = logging.getLogger('error_logger')
success_logger = logging.getLogger('success_logger')


class PersonAPI(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]    

    def get(self, request):
        try:
            person = Person.objects.all()
            serializer = PersonSerializer(person, many=True)
            success_logger.info('Person fetch successfully')
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        except Exception as e:
            error_logger.error("There is error fetching the person")
            return Response(data={'details':"There is an error fetching the posts"}, status=status.HTTP_400_BAD_REQUEST)

    def post(self, request):
        try:
            serializer = PersonSerializer(data=request.data, context={'request':request})
            serializer.is_valid(raise_exception=True)
            serializer.save()
            success_logger.info(f'Person with id{serializer.data.get("id")} created successfully')
            send_mail(
                subject="Person Creation",
                message=f"person created successfully with person id {serializer.data.get('id')}.",
                recipient_list=[request.user.email,],
                fail_silently=False,
            )
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        except Exception as e:
            error_logger.info(f'Error saving data {serializer.errors}')
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PersonDetail(APIView):

    def get(self, request, pk):
        try:
            person = Person.objects.get(pk=pk)
            serializer = PersonSerializer(person)
            success_logger.info('person fetch successfully')
            return Response(serializer.data)
        except Exception as e:
            error_logger.error("There is error fetching the person")
            return Response(data={'detail':'Error retriving data'}, status=status.HTTP_400_BAD_REQUEST)



    def put(self, request, pk):
        try:
            person = self.get_object(pk)
            serializer = PersonSerializer(person, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            success_logger.info('Posts fetch successfully')
            return Response(serializer.data)
        except Exception as e:
            error_logger.error("There is error fetching the person")
            return Response(data={'detail':'Error retriving data'}, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, pk):
        person = self.get_object(pk)
        person.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    # def send_email(self, request):
    #     subject = request.POST.get('subject', "")
    #     message = request.POST.get('message', "")
    #     from_email = request.POST.get('from_email', "")
    #     if subject and message and from_email:
    #         try:
    #             send_mail(subject, message, from_email, ["poojajay@121gmail.com"])
    #             success_logger.info('person fetch successfully')
    #         except Exception as e:
    #             error_logger.error("There is error fetching the person")
    #             return Response(data={'Invalid user found'}, status=status.HTTP_400_BAD_REQUEST)
    #         return Response(status=status.HTTP_200_OK)