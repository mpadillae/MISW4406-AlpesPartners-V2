import os
import uuid
from datetime import datetime
from typing import Dict, Any


class SagaLogger:
    def __init__(self, base_path: str = None):
        if base_path is None:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            self.base_path = os.path.join(current_dir, "..", "..", "..", "..", "logs", "sagas")
        else:
            self.base_path = base_path
        
        os.makedirs(self.base_path, exist_ok=True)
        self.general_log_path = os.path.join(self.base_path, "sagas_general.log")
    
    def _escribir_log(self, archivo: str, mensaje: str):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")[:-3]
        linea_log = f"[{timestamp}] {mensaje}\n"
        
        try:
            with open(archivo, "a", encoding="utf-8") as f:
                f.write(linea_log)
        except Exception as e:
            print(f"Error escribiendo log: {e}")
    
    def iniciar_saga(self, id_saga: uuid.UUID, id_campana: uuid.UUID, id_marca: uuid.UUID, detalles_campana: Dict[str, Any]):
        archivo_saga = os.path.join(self.base_path, f"saga_{id_saga}.log")
        
        mensaje = f"🚀 INICIANDO SAGA"
        mensaje += f"\n   • ID Saga: {id_saga}"
        mensaje += f"\n   • ID Campaña: {id_campana}"
        mensaje += f"\n   • ID Marca: {id_marca}"
        mensaje += f"\n   • Nombre Campaña: {detalles_campana.get('nombre', 'N/A')}"
        mensaje += f"\n   • Presupuesto: ${detalles_campana.get('presupuesto', 0):,.2f}"
        mensaje += f"\n   • Influencers: {len(detalles_campana.get('influencers', []))}"
        mensaje += f"\n   • Tipo: {detalles_campana.get('tipo', 'N/A')}"
        mensaje += "\n" + "="*60
        
        self._escribir_log(archivo_saga, mensaje)
        self._escribir_log(self.general_log_path, f"NUEVA SAGA INICIADA: {id_saga} - Campaña: {detalles_campana.get('nombre', 'N/A')}")
    
    def ejecutar_paso(self, id_saga: uuid.UUID, paso: str, detalles: str = ""):
        archivo_saga = os.path.join(self.base_path, f"saga_{id_saga}.log")
        
        mensaje = f"⚡ EJECUTANDO PASO: {paso.upper()}"
        if detalles:
            mensaje += f"\n   • {detalles}"
        
        self._escribir_log(archivo_saga, mensaje)
    
    def completar_paso(self, id_saga: uuid.UUID, paso: str, resultado: Dict[str, Any]):
        archivo_saga = os.path.join(self.base_path, f"saga_{id_saga}.log")
        
        mensaje = f"✅ PASO COMPLETADO: {paso.upper()}"
        if isinstance(resultado, list):
            mensaje += f"\n   • {len(resultado)} elementos procesados exitosamente"
            for i, res in enumerate(resultado[:3], 1):
                mensaje += f"\n   • Item {i}: {res.get('mensaje', res.get('estado', 'OK'))}"
            if len(resultado) > 3:
                mensaje += f"\n   • ... y {len(resultado) - 3} más"
        else:
            mensaje += f"\n   • {resultado.get('mensaje', resultado.get('estado', 'OK'))}"
        
        self._escribir_log(archivo_saga, mensaje)
    
    def fallar_paso(self, id_saga: uuid.UUID, paso: str, error: str):
        archivo_saga = os.path.join(self.base_path, f"saga_{id_saga}.log")
        
        mensaje = f"❌ PASO FALLIDO: {paso.upper()}"
        mensaje += f"\n   • Error: {error}"
        mensaje += f"\n   • ⚠️  INICIANDO PROCESO DE COMPENSACIÓN..."
        
        self._escribir_log(archivo_saga, mensaje)
        self._escribir_log(self.general_log_path, f"FALLO EN SAGA: {id_saga} - Paso: {paso} - Error: {error}")
    
    def completar_saga(self, id_saga: uuid.UUID, estado_final: str, pasos_completados: list, pasos_compensados: list = None):
        archivo_saga = os.path.join(self.base_path, f"saga_{id_saga}.log")
        
        if estado_final == 'completada':
            mensaje = f"🎉 SAGA COMPLETADA EXITOSAMENTE"
            mensaje += f"\n   • Todos los pasos ejecutados correctamente"
            mensaje += f"\n   • Pasos completados: {', '.join(pasos_completados)}"
            mensaje += f"\n   • Total de pasos: {len(pasos_completados)}"
        elif estado_final == 'compensada':
            mensaje = f"🔄 SAGA COMPENSADA"
            mensaje += f"\n   • Estado restaurado a consistencia"
            mensaje += f"\n   • Pasos que se completaron: {', '.join(pasos_completados) if pasos_completados else 'Ninguno'}"
            mensaje += f"\n   • Pasos compensados: {', '.join(pasos_compensados) if pasos_compensados else 'Ninguno'}"
        else:
            mensaje = f"❓ SAGA FINALIZADA CON ESTADO: {estado_final.upper()}"
        
        mensaje += "\n" + "="*60
        mensaje += f"\n🏁 SAGA {id_saga} FINALIZADA"
        mensaje += "\n" + "="*60
        
        self._escribir_log(archivo_saga, mensaje)
        self._escribir_log(self.general_log_path, f"SAGA FINALIZADA: {id_saga} - Estado: {estado_final.upper()}")
    
    def iniciar_compensacion(self, id_saga: uuid.UUID, mensaje: str):
        archivo_saga = os.path.join(self.base_path, f"saga_{id_saga}.log")
        
        mensaje_log = f"🔄 INICIANDO COMPENSACIÓN"
        mensaje_log += f"\n   • {mensaje}"
        mensaje_log += "\n" + "-"*60
        
        self._escribir_log(archivo_saga, mensaje_log)
    
    def completar_compensacion(self, id_saga: uuid.UUID, paso: str, mensaje: str):
        archivo_saga = os.path.join(self.base_path, f"saga_{id_saga}.log")
        
        mensaje_log = f"✅ COMPENSACIÓN COMPLETADA: {paso.upper()}"
        mensaje_log += f"\n   • {mensaje}"
        
        self._escribir_log(archivo_saga, mensaje_log)
    
    def fallar_compensacion(self, id_saga: uuid.UUID, paso: str, error: str, excepcion: Exception = None):
        archivo_saga = os.path.join(self.base_path, f"saga_{id_saga}.log")
        
        mensaje_log = f"❌ FALLO EN COMPENSACIÓN: {paso.upper()}"
        mensaje_log += f"\n   • Error: {error}"
        if excepcion:
            mensaje_log += f"\n   • Excepción: {type(excepcion).__name__}: {str(excepcion)}"
        
        self._escribir_log(archivo_saga, mensaje_log)
        self._escribir_log(self.general_log_path, f"FALLO COMPENSACIÓN: {id_saga} - Paso: {paso} - Error: {error}")
    
    def log_mensaje(self, id_saga: uuid.UUID, nivel: str, mensaje: str):
        archivo_saga = os.path.join(self.base_path, f"saga_{id_saga}.log")
        
        emoji_map = {
            "INFO": "ℹ️",
            "WARNING": "⚠️", 
            "ERROR": "❌",
            "DEBUG": "🔍"
        }
        
        emoji = emoji_map.get(nivel, "📝")
        mensaje_formateado = f"{emoji} {nivel}: {mensaje}"
        
        self._escribir_log(archivo_saga, mensaje_formateado)
    
    def finalizar_saga(self, id_saga: uuid.UUID, estado_final: str, mensaje: str = ""):
        archivo_saga = os.path.join(self.base_path, f"saga_{id_saga}.log")
        
        emoji_map = {
            'completada': '✅',
            'compensada': '🔄',
            'fallida': '❌'
        }
        
        emoji = emoji_map.get(estado_final, '🏁')
        mensaje_log = f"{emoji} SAGA FINALIZADA - ESTADO: {estado_final.upper()}"
        
        if mensaje:
            mensaje_log += f"\n   • {mensaje}"
        
        mensaje_log += "\n" + "="*60
        mensaje_log += f"\n🏁 SAGA {id_saga} FINALIZADA"
        mensaje_log += "\n" + "="*60
        
        self._escribir_log(archivo_saga, mensaje_log)
        self._escribir_log(self.general_log_path, f"SAGA FINALIZADA: {id_saga} - Estado: {estado_final.upper()}")