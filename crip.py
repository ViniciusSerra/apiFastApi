from passlib.context import CryptContext

# Criar um contexto de senha
pwd_context = CryptContext(schemes=["sha256_crypt"])

# Senha a ser criptografada
senha = '12345678'

# Criar o hash da senha
hashed_senha = pwd_context.hash(senha)

print("Hash da senha:", hashed_senha)

# Verificar a senha
is_valid = pwd_context.verify(senha, hashed_senha)

print("Senha válida:", is_valid)
