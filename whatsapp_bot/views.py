from django.shortcuts import render
# myapp/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import json
import requests
from django.conf import settings
from dotenv import load_dotenv
from rest_framework.permissions import IsAuthenticated ,AllowAny
import os
load_dotenv()

V_token = os.getenv("VERIFY_TOKEN")
W_api = os.getenv("WHATSAPP_API_KEY")
W_number_id = os.getenv("PHONE_NUMBER_ID")

class WhatsAppWebhookAPIView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        try:
            # Parse incoming webhook payload
            payload = json.loads(request.body)
            entry = payload.get("entry", [{}])[0]
            changes = entry.get("changes", [{}])[0]
            value = changes.get("value", {})
            message = value.get("messages", [{}])[0]
            contact_data = value.get("contacts", [{}])[0]
            business_phone_number_id = value.get("metadata", {}).get("phone_number_id")
            phone_number = message.get("from")
            name = contact_data.get("profile", {}).get("name", "User")  # Default to "User" if no name

            # Check if message is text or not
            if not message or message.get("type") != "text":
                return Response({"status": "no text message"}, status=status.HTTP_200_OK)

           

            # Send greeting reply
            greeting = f"Hello {name}! Welcome to Online Savaari Platform . How can we assist you today?"
            reply_payload = {
                "messaging_product": "whatsapp",
                "to": phone_number,
                "text": {"body": greeting},
                "context": {"message_id": message["id"]}  # Reply in context
            }

            print(W_number_id)

            response = requests.post(
                f"https://graph.facebook.com/v18.0/{W_number_id}/messages",
                headers={"Authorization": f"Bearer {W_api}"},
                json=reply_payload
            )

            if response.status_code != 200:
                print(f"Failed to send reply: {response.text}")
                return Response({"status": "failed to send reply", "error": response.text}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            return Response({"status": "success"}, status=status.HTTP_200_OK)

        except json.JSONDecodeError:
            return Response({"status": "invalid payload"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(f"Error: {str(e)}")
            return Response({"status": "error", "detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # Webhook verification (GET request)
    def get(self, request, *args, **kwargs):
        verify_token = V_token
        print("The token is :",verify_token)
        if request.GET.get("hub.verify_token") == verify_token and request.GET.get("hub.mode") == "subscribe" :
            print("This is Verified")
            return Response({request.GET.get("hub.challenge")}, status=status.HTTP_200_OK)
        else :
            print("This is not verified")
            return Response({"status": "verification failed"}, status=status.HTTP_403_FORBIDDEN)
