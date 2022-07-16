from flask import jsonify
from myapp.entity import User
import jwt
from flask_jwt_extended import (
create_access_token, create_refresh_token
)
from myapp.util import checkPassword


class LoginService:
    def login(self, loginRequest):
        user = User.query.filter_by(email=loginRequest.email).first()
        if not user:
            return {
                       "message": "User Not Found"
                   }, 404

        isAuth = checkPassword(user.password, loginRequest.password)

        if isAuth: # 암호화 후 비밀번호 비교하여 일치하면 토큰 발행
            access_token = create_access_token(identity=loginRequest.email)
            refresh_token = create_refresh_token(identity=loginRequest.email)
            return {
                       'Authorization': jsonify(access_token=access_token, refresh_token=refresh_token),
                       # str으로 반환하여 return
                   }, 200

        return {
               "message": "Auth Failed"
        }, 500

    # def logout(self, loginRequest):
    #     user = User(email=userRequest.email,
    #                 password=userRequest.password,
    #                 nickname=userRequest.nickname,
    #                 check__deleted=1)
    #
    #     db.session.add(user)
    #     db.session.commit()
    #     return user