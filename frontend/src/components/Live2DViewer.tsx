import { useAIAvatarContext } from "@/hooks/useAIAvatarContext";
import { useLive2DModel } from "@/hooks/useLive2DModel";
import { useLive2DResize } from "@/hooks/useLive2DResize";
import { AiStateEnum } from "@/hooks/utils/use-ai-state-manager";
import { useForceIgnoreMouse } from "@/hooks/utils/use-force-ignore-mouse";
import { useIpcHandlers } from "@/hooks/utils/use-ipc-handlers";
import { memo, useEffect, useRef } from "react";

interface Live2DProps {
    showSidebar?: boolean;
}

export const Live2D = memo(
    ({ showSidebar }: Live2DProps): React.JSX.Element | null => {
        const { forceIgnoreMouse } = useForceIgnoreMouse();
        const { character, mode, aiState, resetExpression } = useAIAvatarContext();
        const modelInfo = character?.live2d_model_info;
        const internalContainerRef = useRef<HTMLDivElement | null>(null);
        const isPet = mode === 'pet';

        // Get canvasRef from useLive2DResize
        const { canvasRef } = useLive2DResize({
            containerRef: internalContainerRef as React.RefObject<HTMLDivElement>,
            modelInfo,
            showSidebar,
            mode,
        });

        // Pass canvasRef to useLive2DModel
        const { isDragging, handlers } = useLive2DModel({
            character,
            canvasRef: canvasRef as React.RefObject<HTMLCanvasElement>,
            mode,
        });

        // Setup hooks
        useIpcHandlers();

        // Reset expression to default when AI state becomes idle
        useEffect(() => {
            if (aiState === AiStateEnum.IDLE) {
                resetExpression(modelInfo);
            }
        }, [aiState, modelInfo, resetExpression]);

        // Expose setExpression for console testing
        // useEffect(() => {
        //   const testSetExpression = (expressionValue: string | number) => {
        //     const lappAdapter = (window as any).getLAppAdapter?.();
        //     if (lappAdapter) {
        //       setExpression(expressionValue, lappAdapter, `[Console Test] Set expression to: ${expressionValue}`);
        //     } else {
        //       console.error('[Console Test] LAppAdapter not found.');
        //     }
        //   };
        //
        //   // Expose the function to the window object
        //   (window as any).testSetExpression = testSetExpression;
        //   console.log('[Debug] testSetExpression function exposed to window.');
        //
        //   // Cleanup function to remove the function from window when the component unmounts
        //   return () => {
        //     delete (window as any).testSetExpression;
        //     console.log('[Debug] testSetExpression function removed from window.');
        //   };
        // }, [setExpression]);

        const handlePointerDown = (e: React.PointerEvent) => {
            handlers.onMouseDown(e);
        };

        const handleContextMenu = (e: React.MouseEvent) => {
            if (!isPet) {
                return;
            }

            e.preventDefault();
            console.log(
                "[ContextMenu] (Pet Mode) Right-click detected, requesting menu...",
            );
            // window.api?.showContextMenu?.();
        };

        // Conditionally render the Live2D canvas only when the modelInfo is available.
        // This ensures all hooks run unconditionally, but the component does not attempt
        // to render the canvas until it has the necessary data.
        return modelInfo ? (
            <div
                ref={internalContainerRef}
                id="live2d-internal-wrapper"
                style={{
                    width: "100%",
                    height: "100%",
                    pointerEvents: isPet && forceIgnoreMouse ? "none" : "auto",
                    overflow: "hidden",
                    position: "relative",
                    cursor: isDragging ? "grabbing" : "default",
                }}
                onPointerDown={handlePointerDown}
                onContextMenu={handleContextMenu}
                {...handlers}
            >
                <canvas
                    id="canvas"
                    ref={canvasRef}
                    style={{
                        width: "100%",
                        height: "100%",
                        pointerEvents: isPet && forceIgnoreMouse ? "none" : "auto",
                        display: "block",
                        cursor: isDragging ? "grabbing" : "default",
                    }}
                />
            </div>
        ) : null;
    },
);

Live2D.displayName = "Live2D";


