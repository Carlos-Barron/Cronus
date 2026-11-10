import json
import logging
from pathlib import Path

import typer
from pydantic import ValidationError

from cronus.domain.models import UserSchema

# 1. Configuración del Logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# 2. Inicialización de typer

app = typer.Typer(help="CLI para validar archivos JSON.")


@app.command()

def validate_json(
    path: Path = typer.Argument(
        ..., 
        help="Ruta del archivo JSON a validar.",
        exists=True,
        file_okay=True,
        readable=True,
        dir_okay=False
    )
):

    logging.info(file_name := f"Iniciando lectura del archivo: {path}")

    try: 

        # 3. Uso de context manager para abrir el archivo
        with open(path, "r", encoding="utf-8") as file:
            data = json.load(file)
            logging.info("Archivo JSON parseado correctamente")

        # 4. Validación del esquema con Pydantic

        validated_data = UserSchema.model_validate(data)

        logging.info("¡Validación exitosa! El esquema coincide.")
        typer.echo(f"🎉 Datos válidos para el usuario: {validated_data.name}")

    except json.JSONDecodeError as err:
        logging.error(f"Error de formato JSON: {err}")
        raise typer.Exit(code=1)
        
    except ValidationError as err:
        logging.error(f"Error de validación de esquema: {err.json()}")
        typer.echo("❌ El contenido del JSON no cumple con el esquema requerido.")
        raise typer.Exit(code=1)
        
    except Exception as err:
        logging.error(f"Error inesperado: {err}")
        raise typer.Exit(code=1)