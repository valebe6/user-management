from flask import Blueprint, request, jsonify
from marshmallow import ValidationError
from bson.errors import InvalidId

from app.users.schemas import UserCreateSchema, UserUpdateSchema
from app.users import service

users_bp = Blueprint("users", __name__)

create_schema = UserCreateSchema()
update_schema = UserUpdateSchema()


@users_bp.route("", methods=["POST"])
def create():
    """
    Crea un usuario
    ---
    tags:
      - Users
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            required:
              - name
              - email
            properties:
              name:
                type: string
                example: "Valentina"
              email:
                type: string
                example: "val@gmail.com"
              age:
                type: integer
                example: 25
    responses:
      201:
        description: Usuario creado correctamente
        content:
          application/json:
            schema:
              type: object
              properties:
                id: { type: string, example: "656f..." }
                name: { type: string, example: "Valentina" }
                email: { type: string, example: "val@gmail.com" }
                age: { type: integer, example: 25 }
                created_at: { type: string, example: "2025-11-26T12:00:00Z" }
                updated_at: { type: string, nullable: true }
      400:
        description: Error de validación
      409:
        description: Email duplicado
    """
    data = request.get_json(silent=True) or {}
    user_data = create_schema.load(data)  # valida
    user = service.create_user(user_data)
    return jsonify(user), 201


@users_bp.route("", methods=["GET"])
def list_all():
    """
    Lista usuarios con paginación
    ---
    tags:
      - Users
    parameters:
      - in: query
        name: page
        required: false
        schema:
          type: integer
          example: 1
      - in: query
        name: limit
        required: false
        schema:
          type: integer
          example: 10
    responses:
      200:
        description: Lista paginada de usuarios
        content:
          application/json:
            schema:
              type: object
              properties:
                page: { type: integer, example: 1 }
                limit: { type: integer, example: 10 }
                items:
                  type: array
                  items:
                    type: object
                    properties:
                      id: { type: string }
                      name: { type: string }
                      email: { type: string }
                      age: { type: integer, nullable: true }
                      created_at: { type: string }
                      updated_at: { type: string, nullable: true }
      400:
        description: Parámetros de paginación inválidos
    """
    # paginación simple
    try:
        page = int(request.args.get("page", 1))
        limit = int(request.args.get("limit", 10))
        if page < 1 or limit < 1 or limit > 100:
            raise ValueError
    except ValueError:
        raise ValidationError({"page/limit": ["Invalid pagination params"]})

    users = service.list_users(page=page, limit=limit)
    return jsonify({
        "page": page,
        "limit": limit,
        "items": users
    }), 200


@users_bp.route("/<user_id>", methods=["GET"])
def get_one(user_id):
    """
    Obtiene un usuario por ID
    ---
    tags:
      - Users
    parameters:
      - in: path
        name: user_id
        required: true
        schema:
          type: string
          example: "656f1b2c3d4e5f..."
    responses:
      200:
        description: Usuario encontrado
        content:
          application/json:
            schema:
              type: object
              properties:
                id: { type: string }
                name: { type: string }
                email: { type: string }
                age: { type: integer, nullable: true }
                created_at: { type: string }
                updated_at: { type: string, nullable: true }
      404:
        description: Usuario no existe
      400:
        description: ID inválido
    """
    try:
        user = service.get_user(user_id)
    except InvalidId:
        raise ValidationError({"id": ["Invalid user id"]})

    if not user:
        return jsonify({"error": "not_found", "message": "User not found"}), 404
    return jsonify(user), 200


@users_bp.route("/<user_id>", methods=["PUT", "PATCH"])
def update(user_id):
    """
    Actualiza un usuario por ID
    ---
    tags:
      - Users
    parameters:
      - in: path
        name: user_id
        required: true
        schema:
          type: string
          example: "656f1b2c3d4e5f..."
    requestBody:
      required: true
      content:
        application/json:
          schema:
            type: object
            properties:
              name:
                type: string
                example: "otro usuario"
              email:
                type: string
                example: "otheruser@gmail.com"
              age:
                type: integer
                example: 30
    responses:
      200:
        description: Usuario actualizado correctamente
        content:
          application/json:
            schema:
              type: object
              properties:
                id: { type: string }
                name: { type: string }
                email: { type: string }
                age: { type: integer, nullable: true }
                created_at: { type: string }
                updated_at: { type: string, nullable: true }
      404:
        description: Usuario no existe
      400:
        description: Error de validación o ID inválido
      409:
        description: Email duplicado
    """
    data = request.get_json(silent=True) or {}
    user_data = update_schema.load(data)

    try:
        user = service.update_user(user_id, user_data)
    except InvalidId:
        raise ValidationError({"id": ["Invalid user id"]})

    if not user:
        return jsonify({"error": "not_found", "message": "User not found"}), 404
    return jsonify(user), 200


@users_bp.route("/<user_id>", methods=["DELETE"])
def delete(user_id):
    """
    Elimina un usuario por ID
    ---
    tags:
      - Users
    parameters:
      - in: path
        name: user_id
        required: true
        schema:
          type: string
          example: "656f1b2c3d4e5f..."
    responses:
      204:
        description: Usuario eliminado correctamente (sin contenido)
      404:
        description: Usuario no existe
      400:
        description: ID inválido
    """
    try:
        ok = service.delete_user(user_id)
    except InvalidId:
        raise ValidationError({"id": ["Invalid user id"]})

    if not ok:
        return jsonify({"error": "not_found", "message": "User not found"}), 404
    return "", 204
