;;; Directory Local Variables
;;; For more information see (info "(emacs) Directory Variables")

((python-mode . ((eval . (setq lsp-python-ms-extra-paths ["/snap/blender/161/2.93/scripts/modules/"]))
                 (eval . (message  "Blender Local dir variables executed for python mode."))))

 (nil  . ((pyvenv-workon . "manim")
          (eval . (setq projectile-project-root  "/home/bachir/Dropbox/Youtube/blender-anim/"))
          (eval . (git-auto-commit-mode 1)))))
