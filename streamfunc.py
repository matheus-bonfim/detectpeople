import cv2

def watchStream(videoCh, ret, frame):
    if(ret):
        frame = cv2.resize(frame, (1280,720))
        # desenha linha virtual
        cv2.line(frame, videoCh.p_line1, videoCh.p_line2, (0, 255, 255), 2)

        # total de pessoas que cruzaram
        cv2.putText(frame, f'Entraram: {videoCh.countAB if videoCh.direction else videoCh.countBA}', (400, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

        cv2.putText(frame,f'Sairam: {videoCh.countBA if videoCh.direction else videoCh.countAB}', (700, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)

        cv2.rectangle(frame, (0, 130), (1280, 720), (0, 255, 0), 2)
#(130, 720, 0, 720)
        cv2.imshow("Contagem de Pessoas na Linha", frame)
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            return False

    return True