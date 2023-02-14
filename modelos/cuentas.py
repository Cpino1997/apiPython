class Cuenta:
    def __init__(self, _id, usuario, password, correo, roles):
        self._id = _id
        self.usuario = usuario
        self.password = password
        self.correo = correo
        self.roles = roles

    def to_json(self):
        return {
            'id': self._id,
            'usuario': self.usuario,
            'password': self.password,
            'correo': self.correo,
            'roles': self.roles
        }