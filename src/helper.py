from datetime import datetime

def tlog(componentName, text):
    timestamp = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    return (f'[{timestamp}] [{componentName}]: {text}\n')