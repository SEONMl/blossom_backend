from flask import request, Response
from flask_jwt_extended import jwt_required
from flask_restx import Namespace
from flask_restx import Resource

from myapp.service.PhotoService import deletePhotosById, savePhoto, \
    getPhotosFromBucketByUserId, getPhotoByPhotoId

ALLOWED_EXTENSION = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])

nsPhoto = Namespace('api/photos')


@nsPhoto.route('')
class PhotoController(Resource):
    @nsPhoto.param('userId')  # Integer로 바꿔야 함ㅠ
    @jwt_required(locations=['cookies'])
    def get(self):
        """User ID에 해당하는 사진을 조회한다."""
        user_id = request.args.get('userId')
        url_list = getPhotosFromBucketByUserId(user_id)
        return url_list

    def post(self):
        """클라이언트로부터 요청받은 흑백사진을 저장하고 컬러화한다."""
        reqFile = request.files['file']
        savePhoto(reqFile, userId=1)
        return Response("created", status=201)

    def delete(self):
        """요청받은 사진을 삭제 처리한다."""
        targets = request.get_json()
        deletePhotosById(targets['id'])
        return Response(targets, status=204)


@nsPhoto.route('/<int:photo_id>')
class PhotoSingleController(Resource):
    @jwt_required()
    def get(self, photo_id):
        """photo_id에 해당하는 사진 단일 조회"""
        result = getPhotoByPhotoId(photo_id)
        return result, 200
