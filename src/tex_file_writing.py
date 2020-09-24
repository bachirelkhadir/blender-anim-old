import os
import hashlib
from pathlib import Path
import bpy
import bmesh
import logging
log = logging.getLogger(__name__)
import src.consts as consts
import src.utils as utils


def tex_hash(expression, template_tex_file_body):
    id_str = str(expression + template_tex_file_body)
    hasher = hashlib.sha256()
    hasher.update(id_str.encode())
    # Truncating at 16 bytes for cleanliness
    return hasher.hexdigest()[:16]


def tex_to_svg_file(expression, template_tex_file_body):

    tex_file = generate_tex_file(expression, template_tex_file_body)
    dvi_file = tex_to_dvi(tex_file)
    svg_filepath = dvi_to_svg(dvi_file)
    log.debug(f"{expression} -> {svg_filepath}")
    return svg_filepath


def generate_tex_file(expression, template_tex_file_body):
    result = os.path.join(
        consts.TEX_DIR,
        tex_hash(expression, template_tex_file_body)
    ) + ".tex"
    if not os.path.exists(result):
        print("Writing \"%s\" to %s" % (
            "".join(expression), result
        ))
        new_body = template_tex_file_body.replace(
            consts.TEX_TEXT_TO_REPLACE, expression
        )
        with open(result, "w", encoding="utf-8") as outfile:
            outfile.write(new_body)
    return result


def tex_to_dvi(tex_file):
    result = tex_file.replace(".tex", ".dvi" if not consts.TEX_USE_CTEX else ".xdv")
    result = Path(result).as_posix()
    tex_file = Path(tex_file).as_posix()
    tex_dir = Path(consts.TEX_DIR).as_posix()
    if not os.path.exists(result):
        commands = [
            "latex",
            "-interaction=batchmode",
            "-halt-on-error",
            "-output-directory=\"{}\"".format(tex_dir),
            "\"{}\"".format(tex_file),
            ">",
            os.devnull
        ] if not consts.TEX_USE_CTEX else [
            "xelatex",
            "-no-pdf",
            "-interaction=batchmode",
            "-halt-on-error",
            "-output-directory=\"{}\"".format(tex_dir),
            "\"{}\"".format(tex_file),
            ">",
            os.devnull
        ]
        exit_code = os.system(" ".join(commands))
        if exit_code != 0:
            log_file = tex_file.replace(".tex", ".log")
            raise Exception(
                ("Latex error converting to dvi. " if not consts.TEX_USE_CTEX
                else "Xelatex error converting to xdv. ") +
                "See log output above or the log file:\n %s" % log_file +
                "or tex file:\n File \"%s\", line 1" % tex_file)
    return result


def dvi_to_svg(dvi_file, regen_if_exists=False):
    """
    Converts a dvi, which potentially has multiple slides, into a
    directory full of enumerated pngs corresponding with these slides.
    Returns a list of PIL Image objects for these images sorted as they
    where in the dvi
    """
    result = dvi_file.replace(".dvi" if not consts.TEX_USE_CTEX else ".xdv", ".svg")
    result = Path(result).as_posix()
    result_cleaned = result[:-4]+"-cleaned.svg"
    dvi_file = Path(dvi_file).as_posix()
    if True or not os.path.exists(result):

        # dvi -> svg
        commands = [
            "dvisvgm",
            "\"{}\"".format(dvi_file),
            "-n",
            "-v",
            "0",
            "-o",
            "\"{}\"".format(result),
            ">",
            os.devnull
        ]
        log.debug("dvi -> svg")
        log.debug(" ".join(commands))
        os.system(" ".join(commands))


        # clean svg
        commands = [
            consts.SVG_CLEANER_BIN,
            "\"{}\"".format(result),
            "\"{}\"".format(result_cleaned),
            ">",
            os.devnull
        ]
        log.debug("Clean svg")
        log.debug(" ".join(commands))
        os.system(" ".join(commands))
    return result_cleaned



def tex_to_bpy(expression, tex_collection, template_tex_file_body=None):
    """
    Converts a tex to blender object
    """
    log.info(f"Tex -> Bpy ({expression})")
    if template_tex_file_body == None:
        template_tex_file_body = open(consts.TEMPLATE_TEX_FILE).read()

    # convert tex to svg
    svg_filepath = tex_to_svg_file(expression, template_tex_file_body)

    # load svg into blender
    new_collection = utils.import_svg_in_blender_as_collection(svg_filepath)

    log.debug(f"{expression} -> collection {new_collection}")
    
    svg_collection = bpy.data.collections[new_collection]
    #svg_collection.name = "SVG " + expression


    # join all meshes into one object
    # TODO: preserve material while joining
    obs = svg_collection.objects

    parent = obs[0]
    bpy.ops.object.select_all(action='DESELECT')
    bpy.context.view_layer.objects.active = parent
    for c in obs:
        c.select_set(state=True)
    bpy.ops.object.join()
    parent.scale *= 500
    tex_collection.objects.link(parent)

    # remove unndeeded collection
    utils.remove_bpy_collection(svg_collection)

    return parent


