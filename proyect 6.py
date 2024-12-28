import aiohttp
import os
@bot.command()
async def check(ctx, link=None):
    if ctx.message.attachments:  # Manejo de archivos adjuntos
        for attachment in ctx.message.attachments:
            file_name = attachment.filename
            file_url = attachment.url
            await attachment.save(f"./{file_name}")
            await ctx.send(f"Guardé la imagen en ./{file_name}")
    elif link:  # Manejo de enlaces proporcionados como argumento
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get(link) as response:
                    if response.status == 200:
                        content_disposition = response.headers.get("Content-Disposition", "")
                        file_name = (
                            content_disposition.split("filename=")[-1].strip('"')
                            if "filename=" in content_disposition
                            else os.path.basename(link)
                        )
                        file_path = f"./{file_name}"
                        with open(file_path, "wb") as f:
                            f.write(await response.read())
                        await ctx.send(f"Guardé el archivo del enlace en {file_path}")
                    else:
                        await ctx.send(f"No se pudo descargar el archivo. Estado HTTP: {response.status}")
            except Exception as e:
                await ctx.send(f"Hubo un error al descargar el archivo: {e}")
    else:
        await ctx.send("Por favor, sube una imagen o proporciona un enlace.")
