# limpiar.py
# Archivo para limpiar residuos de la compilación de manera rápida usando múltiples hilos.

import os
import shutil
import threading

def eliminar_carpeta(carpeta):
	"""Elimina una carpeta si existe."""
	if os.path.exists(carpeta):
		shutil.rmtree(carpeta, ignore_errors=True)
		print(f"✅ Carpeta eliminada: {carpeta}")
	else:
		print(f"⚠️ Carpeta no encontrada: {carpeta}")

def eliminar_archivos_por_extension(extension):
	"""Elimina archivos con una extensión específica en el directorio actual y subdirectorios."""
	for carpeta_raiz, _, archivos in os.walk("."):
		archivos_a_eliminar = [os.path.join(carpeta_raiz, archivo) for archivo in archivos if archivo.endswith(extension)]
		
		def eliminar_archivo(ruta_archivo):
			try:
				os.remove(ruta_archivo)
				print(f"🗑️ Archivo eliminado: {ruta_archivo}")
			except Exception as e:
				print(f"❌ No se pudo eliminar {ruta_archivo}: {e}")

		# Ejecutar en hilos para mayor velocidad
		threads = [threading.Thread(target=eliminar_archivo, args=(archivo,)) for archivo in archivos_a_eliminar]
		
		for thread in threads:
			thread.start()

		for thread in threads:
			thread.join()

def limpiar_proyecto():
	"""Elimina carpetas y archivos innecesarios del proyecto usando múltiples hilos."""
	print("🔍 Iniciando limpieza del proyecto...\n")

	# Ejecutar eliminación de carpetas en hilos
	carpetas = ["dist", "build", "__pycache__"]
	threads = [threading.Thread(target=eliminar_carpeta, args=(carpeta,)) for carpeta in carpetas]

	for thread in threads:
		thread.start()

	for thread in threads:
		thread.join()

	# Eliminar archivos en paralelo
	extensiones = [".pyc", ".pyo"]
	threads = [threading.Thread(target=eliminar_archivos_por_extension, args=(ext,)) for ext in extensiones]

	for thread in threads:
		thread.start()

	for thread in threads:
		thread.join()

	print("\n✅ Limpieza completada.")

if __name__ == "__main__":
	limpiar_proyecto()
