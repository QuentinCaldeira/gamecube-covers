from PIL import Image
import os

def resize_and_compress_image(input_path, output_path, target_width, target_height, max_size_kb, output_format):
    """
    Redimensionne une image pour correspondre à une taille fixe et la compresse pour atteindre la taille maximale spécifiée.

    :param input_path: Chemin de l'image d'entrée
    :param output_path: Chemin de l'image de sortie
    :param target_width: Largeur cible en pixels
    :param target_height: Hauteur cible en pixels
    :param max_size_kb: Taille maximale en KB
    :param output_format: Format de sortie ("JPEG" ou "PNG")
    """
    with Image.open(input_path) as img:
        if img.mode == "RGBA":
            img = img.convert("RGB")

        img = img.resize((target_width, target_height), Image.LANCZOS)

        if output_format.upper() == "JPEG":
            quality = 95
            while quality > 10:
                img.save(output_path, "JPEG", quality=quality)
                output_size_kb = os.path.getsize(output_path) / 1024

                if output_size_kb <= max_size_kb:
                    break

                quality -= 5

            if quality <= 10:
                print(f"Impossible de compresser {input_path} à moins de {max_size_kb} KB tout en maintenant une qualité acceptable.")
        elif output_format.upper() == "PNG":
            # PNG ne permet pas de régler directement la qualité, mais nous utilisons une compression optimisée.
            img.save(output_path, "PNG", optimize=True)
            output_size_kb = os.path.getsize(output_path) / 1024
            if output_size_kb > max_size_kb:
                print(f"Impossible de compresser {input_path} à moins de {max_size_kb} KB avec le format PNG.")

def process_folder_recursive(input_folder, output_folder, target_width, target_height, max_size_kb, output_format):
    """
    Parcourt un dossier récursivement pour redimensionner et compresser toutes les images tout en répliquant la structure des dossiers.

    :param input_folder: Chemin du dossier d'entrée
    :param output_folder: Chemin du dossier de sortie
    :param target_width: Largeur cible en pixels
    :param target_height: Hauteur cible en pixels
    :param max_size_kb: Taille maximale en KB
    :param output_format: Format de sortie ("JPEG" ou "PNG")
    """
    for root, _, files in os.walk(input_folder):
        # Réplique la structure des dossiers
        relative_path = os.path.relpath(root, input_folder)
        current_output_folder = os.path.join(output_folder, relative_path)
        os.makedirs(current_output_folder, exist_ok=True)

        for filename in files:
            input_path = os.path.join(root, filename)
            output_path = os.path.join(current_output_folder, os.path.splitext(filename)[0] + (".jpg" if output_format.upper() == "JPEG" else ".png"))

            if filename.lower().endswith((".jpg", ".jpeg", ".png")):
                try:
                    resize_and_compress_image(input_path, output_path, target_width, target_height, max_size_kb, output_format)
                    print(f"Traitement terminé pour : {input_path}")
                except Exception as e:
                    print(f"Erreur lors du traitement de {input_path}: {e}")

if __name__ == "__main__":
    input_folder = "untouched"  # Répertoire des images d'entrée
    output_folder = "retouched"  # Répertoire des images de sortie

    process_folder_recursive(
        input_folder=input_folder,
        output_folder=output_folder,
        target_width=506,
        target_height=718,
        max_size_kb=250,
        output_format="JPEG"
    )