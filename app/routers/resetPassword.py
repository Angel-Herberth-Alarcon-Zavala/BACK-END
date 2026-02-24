from fastapi import APIRouter, HTTPException

# Librerías para envío de correo
from email.message import EmailMessage
import random
import smtplib

# Imports de routers y base de datos
from app.database import get_db
from app.schemas import EmailRequest, codeRequest, ResetPasswordRequest

router = APIRouter(
    prefix="/reset-password",
    tags=["ResetPassword"]
)

def enviar_correo_html(destinatario: str, codigo: str):
    REMITENTE = "tu_correo@gmail.com" 
    PASSWORD = "tu_contraseña_de_aplicacion" 

    msg = EmailMessage()
    msg['Subject'] = 'Código de Recuperación de Cuenta'
    msg['From'] = REMITENTE
    msg['To'] = destinatario

    # HTML de correo de recuperación
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <body style="font-family: Arial, sans-serif; background-color: #f9fafb; padding: 20px;">
        <div style="max-w: 500px; margin: 0 auto; background-color: white; padding: 30px; border-radius: 10px; border: 1px solid #e5e7eb;">
            <h2 style="color: #1e40af; text-align: center;">Recuperación de Contraseña</h2>
            <p style="color: #374151; font-size: 16px;">Hola,</p>
            <p style="color: #374151; font-size: 16px;">Hemos recibido una solicitud para restablecer la contraseña de tu cuenta. Usa el siguiente código de 4 dígitos para continuar:</p>
            
            <div style="text-align: center; margin: 30px 0;">
                <span style="font-size: 32px; font-weight: bold; letter-spacing: 5px; color: #047857; background-color: #d1fae5; padding: 10px 20px; border-radius: 8px;">
                    {codigo}
                </span>
            </div>
            
            <p style="color: #6b7280; font-size: 14px;">Si no solicitaste este cambio, puedes ignorar este correo de forma segura.</p>
        </div>
    </body>
    </html>
    """
    
    msg.set_content("Tu cliente de correo no soporta HTML. Tu código es: " + codigo)
    msg.add_alternative(html_content, subtype='html')

    try:
        # Conexión al servidor de Gmail
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(REMITENTE, PASSWORD)
            smtp.send_message(msg)
        return True
    except Exception as e:
        print(f"Error al enviar correo: {e}")
        return False

@router.post("/solicitar-codigo")
def solicitar_codigo(req: EmailRequest):
    usuario_existe = any(u["email"] == req.email for u in USUARIOS)
    if not usuario_existe:
        raise HTTPException(status_code=404, detail="Correo no encontrado en el sistema")

    codigo_generado = str(random.randint(1000, 9999))
    CODIGOS_RECUPERACION[req.email] = codigo_generado
    
    print(f"🔑 CÓDIGO GENERADO PARA {req.email}: {codigo_generado}")

    # exito = enviar_correo_html(req.email, codigo_generado)
    # if not exito:
    #     raise HTTPException(status_code=500, detail="Error al enviar el correo")

    return {"success": True, "message": "Código generado y enviado"}

@router.post("/verificar-codigo")
def verificar_codigo(req: codeRequest):
    if req.email in CODIGOS_RECUPERACION and req.code in CODIGOS_RECUPERACION.values():
        return{
            "success": True,
            "message": "Código verificado."
        }
    raise HTTPException(status_code=404, detail="Código incorrecto")

@router.post("/cambiar-password")
def cambiar_password(req: ResetPasswordRequest):
    for user in USUARIOS:
        if user["email"] == req.email:
            user["password"] = req.nuevo_password

            if req.email in CODIGOS_RECUPERACION:
                del CODIGOS_RECUPERACION[req.email]
            return {"success": True, "message": "Contraseña actualizada con éxito"}
        
    raise HTTPException(status_code=404, detail="Usuario no encontrado")