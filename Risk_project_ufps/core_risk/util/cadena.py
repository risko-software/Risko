def limpiar_descripcion(descripcion: str):
    descripcion = descripcion.replace("'", "")
    descripcion = descripcion.replace("\"", "")
    descripcion = descripcion.replace('\n', ' ')
    descripcion = descripcion.replace('\r', '')
    return descripcion
