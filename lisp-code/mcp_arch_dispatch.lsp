;;; ==========================================================================
;;; mcp_arch_dispatch.lsp — AutoCAD / AutoCAD LT 2024+ 2D Architecture Dispatcher
;;; Compatible with Full AutoCAD and AutoCAD LT 2024+ (Windows)
;;; Load via APPLOAD and invoke (c:mcp-arch-setup) or (c:mcp-arch-dispatch)
;;; ==========================================================================

(defun c:mcp-arch-setup ( / )
  (setvar "CMDECHO" 0)
  (command "._-UNITS" "2" "2" "1" "2" "0" "N")
  ;; Create AIA Architectural Layers with standard colors
  (command "._-LAYER"
    "M" "A-GRID"      "C" "8"   "A-GRID"
    "M" "A-GRID-IDEN" "C" "7"   "A-GRID-IDEN"
    "M" "A-COLS"      "C" "7"   "A-COLS"
    "M" "A-WALL-FULL" "C" "7"   "A-WALL-FULL"
    "M" "A-WALL-PRHT" "C" "2"   "A-WALL-PRHT"
    "M" "A-WALL-PATT" "C" "253" "A-WALL-PATT"
    "M" "A-DOOR"      "C" "3"   "A-DOOR"
    "M" "A-DOOR-SWNG" "C" "8"   "A-DOOR-SWNG"
    "M" "A-GLAZ"      "C" "4"   "A-GLAZ"
    "M" "A-GLAZ-SILL" "C" "8"   "A-GLAZ-SILL"
    "M" "A-STAIR"     "C" "3"   "A-STAIR"
    "M" "A-FIXT"      "C" "5"   "A-FIXT"
    "M" "A-FURN"      "C" "252" "A-FURN"
    "M" "A-OVER"      "C" "1"   "A-OVER"
    "M" "A-ROOF"      "C" "7"   "A-ROOF"
    "M" "A-ELEV-PROF" "C" "7"   "A-ELEV-PROF"
    "M" "E-LITE"      "C" "2"   "E-LITE"
    "M" "M-HVAC"      "C" "4"   "M-HVAC"
    "M" "S-FOOT"      "C" "6"   "S-FOOT"
    "M" "S-BEAM"      "C" "3"   "S-BEAM"
    "M" "A-ANNO-DIMS" "C" "6"   "A-ANNO-DIMS"
    "M" "A-ANNO-TEXT" "C" "7"   "A-ANNO-TEXT"
    "M" "A-ANNO-SYMB" "C" "7"   "A-ANNO-SYMB"
    "M" "A-TTLB"      "C" "7"   "A-TTLB"
    ""
  )
  (princ "\n=== Architect-CAD-MCP v1.0.0: 24 AIA Architectural Layers initialized ===")
  (princ)
)

(defun mcp-arch-draw-wall (x1 y1 x2 y2 thick / )
  (command "._-LAYER" "S" "A-WALL-FULL" "")
  (if (< (abs (- y2 y1)) 0.001)
    (command "._RECTANG" (list (min x1 x2) (- y1 (* thick 0.5))) (list (max x1 x2) (+ y1 (* thick 0.5))))
    (command "._RECTANG" (list (- x1 (* thick 0.5)) (min y1 y2)) (list (+ x1 (* thick 0.5)) (max y1 y2)))
  )
)

(defun mcp-arch-draw-door (x y width orient / )
  (command "._-LAYER" "S" "A-DOOR" "")
  (if (equal orient "north")
    (progn
      (command "._RECTANG" (list x y) (list (+ x 0.05) (+ y width)))
      (command "._-LAYER" "S" "A-DOOR-SWNG" "")
      (command "._ARC" "C" (list x y) (list (+ x width) y) (list x (+ y width)))
    )
    (progn
      (command "._RECTANG" (list x (- y width)) (list (+ x 0.05) y))
      (command "._-LAYER" "S" "A-DOOR-SWNG" "")
      (command "._ARC" "C" (list x y) (list x (- y width)) (list (+ x width) y))
    )
  )
)

(princ "\n=== Architect-CAD-MCP AutoLISP Dispatcher v1.0.0 Loaded. Run (c:mcp-arch-setup) ===\n")
(princ)
