import os
import hashlib
from pathlib import Path
import bpy

import src.consts as consts



def tex_hash(expression, template_tex_file_body):
    id_str = str(expression + template_tex_file_body)
    hasher = hashlib.sha256()
    hasher.update(id_str.encode())
    # Truncating at 16 bytes for cleanliness
    return hasher.hexdigest()[:16]


def tex_to_svg_file(expression, template_tex_file_body):

    tex_file = generate_tex_file(expression, template_tex_file_body)
    dvi_file = tex_to_dvi(tex_file)
    return dvi_to_svg(dvi_file)


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
                ("Latex error converting to dvi. " if not TEX_USE_CTEX
                else "Xelatex error converting to xdv. ") +
                "See log output above or the log file: %s" % log_file)
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
    dvi_file = Path(dvi_file).as_posix()
    if not os.path.exists(result):
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
        os.system(" ".join(commands))
    return result



def tex_to_bpy(expression, template_tex_file_body=None):
    if template_tex_file_body == None:
        template_tex_file_body = open(consts.TEMPLATE_TEX_FILE).read()
    svg_filepath = tex_to_svg_file(expression, template_tex_file_body)
    names_pre_import = set([ o.name for o in bpy.context.scene.objects ])
    bpy.ops.import_curve.svg(filepath=svg_filepath)
    names_post_import = set([ o.name for o in bpy.context.scene.objects ])
    newcurves = list(names_post_import.difference( names_pre_import ))#.pop()
    curve_parent = bpy.data.objects[newcurves[0]]
    for newcurve in newcurves[1:]:
        bpy.data.objects[newcurve].parent = curve_parent 

    curve_parent.scale *= 1000
    return curve_parent


