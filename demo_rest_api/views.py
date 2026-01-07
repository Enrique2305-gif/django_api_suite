from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

import uuid

# Simulación de base de datos local en memoria
data_list = []

# Añadiendo algunos datos de ejemplo para probar el GET
data_list.append({'id': str(uuid.uuid4()), 'name': 'User01', 'email': 'user01@example.com', 'is_active': True})
data_list.append({'id': str(uuid.uuid4()), 'name': 'User02', 'email': 'user02@example.com', 'is_active': True})
data_list.append({'id': str(uuid.uuid4()), 'name': 'User03', 'email': 'user03@example.com', 'is_active': False}) # Ejemplo de item inactivo

def get_record_by_id(record_id):
    for pos, rec in enumerate(records):
        if rec["id"] == record_id:
            return pos, rec
    return None, None


class DemoRestApi(APIView):
    name = "Demo REST API"
    def get(self, request):

      # Filtra la lista para incluir solo los elementos donde 'is_active' es True
      active_items = [item for item in data_list if item.get('is_active', False)]
      return Response(active_items, status=status.HTTP_200_OK)

    def post(self, request):
      data = request.data

      # Validación mínima
      if 'name' not in data or 'email' not in data:
         return Response({'error': 'Faltan campos requeridos.'}, status=status.HTTP_400_BAD_REQUEST)

      data['id'] = str(uuid.uuid4())
      data['is_active'] = True
      data_list.append(data)

      return Response({'message': 'Dato guardado exitosamente.', 'data': data}, status=status.HTTP_201_CREATED)
      

class DemoRestApiItem(APIView):
     
    def put(self, request, item_id):
        payload = request.data
        idx, record = get_record_by_id(item_id)

        if record is None:
            return Response(
                {"message": "No se encontró el recurso solicitado."},
                status=status.HTTP_404_NOT_FOUND
            )

        if not payload.get("name") or not payload.get("email"):
            return Response(
                {"message": "PUT requiere name y email (reemplazo total)."},
                status=status.HTTP_400_BAD_REQUEST
            )

        records[idx] = {
            "id": item_id,                     # ID inmutable
            "name": payload["name"],
            "email": payload["email"],
            "is_active": record["is_active"]   # conserva estado
        }

        return Response(
            {"message": "Recurso reemplazado exitosamente.", "data": records[idx]},
            status=status.HTTP_200_OK
        )

    def patch(self, request, item_id):
        payload = request.data
        idx, record = get_record_by_id(item_id)

        if record is None:
            return Response(
                {"message": "Recurso no encontrado."},
                status=status.HTTP_404_NOT_FOUND
            )

        if "id" in payload and payload["id"] != item_id:
            return Response(
                {"message": "El identificador no puede ser modificado."},
                status=status.HTTP_400_BAD_REQUEST
            )

        updated = {
            **record,
            **{k: v for k, v in payload.items() if k in ["name", "email", "is_active"]}
        }

        records[idx] = updated

        return Response(
            {"message": "Campos actualizados correctamente.", "data": updated},
            status=status.HTTP_200_OK
        )

    def delete(self, request, item_id):
        idx, record = get_record_by_id(item_id)

        if record is None:
            return Response(
                {"message": "Recurso inexistente."},
                status=status.HTTP_404_NOT_FOUND
            )

        if not record["is_active"]:
            return Response(
                {"message": "El recurso ya estaba desactivado."},
                status=status.HTTP_200_OK
            )

        record["is_active"] = False
        records[idx] = record

        return Response(
            {"message": "Recurso desactivado correctamente.", "data": record},
            status=status.HTTP_200_OK
        )