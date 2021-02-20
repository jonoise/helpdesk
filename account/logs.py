def rol_Log(Log, request_user, rol):
    header = f'Rol seleccionado: {rol}'
    body = f'Se ha hecho un cambio de rol.'
    
    new_log = Log(user=request_user, header=header, body=body)
    new_log.save()