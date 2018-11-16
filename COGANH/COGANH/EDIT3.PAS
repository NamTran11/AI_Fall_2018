{ Copyright (c) 2002 by Nguyen Tan Dat. All rights reserved }
Uses Graph, NTD, MouseGr, Crt, GameMenu, OpenWind,
     InfGame, LoadFile, GameSave, Viet_hoa, Dos;
Var x, y, LastX, LastY : Integer;
    OddClick, ClickLeft : Boolean;
    EnableMove : Boolean;
    QCActi : Byte;
    Nguoichoi : Boolean;
    DangMo : Boolean;
    Ch : Char;
    NameHDFile : String;
    OpenX, OpenY : Integer;

(*----------------------------------*)
Procedure CloseProgram;
Begin
     FreeMemPtrMenu(PtrMenu);
     DongBanco;
End;
(*----------------------------------*)
{ Kiem tra co quan cua doi phuong di den diem mo hay khong ? }
Function CoDoiphuongDiden(X,Y : Integer; QC : Byte) : Boolean;
{ X, Y la toa do cua quan co doi phuong di den,
  Qc la loai quan co di den }
Begin
     If Odd(X + Y) then
        CoDoiphuongDiden := (Quanco[ X,Y-1].Enable and (Quanco[ X,Y-1].Qc = Qc) and (Y-1 > 0)) Or
                            (Quanco[ X,Y+1].Enable and (Quanco[ X,Y+1].Qc = Qc) and (Y+1 < 6)) Or
                            (Quanco[ X-1,Y].Enable and (Quanco[ X-1,Y].Qc = Qc) and (X-1 > 0)) Or
                            (Quanco[ X+1,Y].Enable and (Quanco[ X+1,Y].Qc = Qc) and (X+1 < 6))
     Else
        CoDoiphuongDiden := (Quanco[ X,Y-1].Enable and (Quanco[ X,Y-1].Qc = Qc) and (Y-1 > 0)) Or
                            (Quanco[ X,Y+1].Enable and (Quanco[ X,Y+1].Qc = Qc) and (Y+1 < 6)) Or
                            (Quanco[ X-1,Y].Enable and (Quanco[ X-1,Y].Qc = Qc) and (X-1 > 0)) Or
                            (Quanco[ X+1,Y].Enable and (Quanco[ X+1,Y].Qc = Qc) and (X+1 < 6)) Or

                            (Quanco[ X-1,Y-1].Enable and (Quanco[ X-1,Y-1].Qc = Qc) and (X-1 > 0) and (Y-1 > 0)) Or
                            (Quanco[ X+1,Y+1].Enable and (Quanco[ X+1,Y+1].Qc = Qc) and (X+1 < 6) and (Y+1 < 6)) Or
                            (Quanco[ X-1,Y+1].Enable and (Quanco[ X-1,Y+1].Qc = Qc) and (X-1 > 0) and (Y+1 < 6)) Or
                            (Quanco[ X+1,Y-1].Enable and (Quanco[ X+1,Y-1].Qc = Qc) and (X+1 < 6) and (Y-1 > 0))End;
(*----------------------------------*)
Function Ganhduoc(X,Y : Integer; Qc : Byte) : Boolean;
Var Gd : Boolean;
Begin
     Gd := False;
     If Not CoDoiphuongDiden(X,Y,Qc) then
     Begin
          Ganhduoc := False;
          Exit;
     End;
     If Odd(X + Y) then
     Begin
         If (X - 1 > 0) and (X + 1 < 6) then
            If (ABS(Quanco[X - 1,Y].QC - QC) = 1) and (ABS(Quanco[X + 1,Y].QC - QC) = 1) and
               (Quanco[X - 1,Y].Enable) and (Quanco[X + 1,Y].Enable) then
                Gd := True;
         If (Y - 1 > 0) and (Y + 1 < 6) and Not Gd then
            If (ABS(Quanco[X,Y-1].QC - QC) = 1) and (ABS(Quanco[X,Y+1].QC - QC) = 1) and
               (Quanco[X,Y - 1].Enable) and (Quanco[X ,Y + 1].Enable) then
               Gd := True;
     End
     Else
     Begin
         If (X - 1 > 0) and (X + 1 < 6) then
            If (ABS(Quanco[X-1,Y].QC - QC) = 1) and (ABS(Quanco[X+1,Y].QC - QC) = 1) and
               (Quanco[X - 1,Y].Enable) and (Quanco[X + 1,Y].Enable) then
               Gd := True;

         If (Y - 1 > 0) and (Y + 1 < 6) and Not Gd then
            If (ABS(Quanco[X,Y-1].QC - QC) = 1) and (ABS(Quanco[X,Y+1].QC - QC) = 1) and
               (Quanco[X,Y - 1].Enable) and (Quanco[X ,Y + 1].Enable) then
                Gd := True;

         If (X - 1 > 0) and (X + 1 < 6) and (Y - 1 > 0) and (Y + 1 < 6)
            and Not Gd then
            If (ABS(Quanco[X-1,Y-1].QC - QC) = 1) and (ABS(Quanco[X+1,Y+1].QC - QC) = 1) and
               (Quanco[X - 1,Y - 1].Enable) and (Quanco[X + 1,Y + 1].Enable) then
               Gd := True
            Else
               If (ABS(Quanco[X-1,Y+1].QC - QC) = 1) and (ABS(Quanco[X+1,Y-1].QC - QC) = 1) and
                  (Quanco[X + 1,Y - 1].Enable) and (Quanco[X - 1,Y + 1].Enable) then
                  Gd := True;
     End;
     Ganhduoc := Gd;
End;
(*----------------------------------*)
Procedure ShowOpen(X,Y : Integer; Qc : Byte);
{ X, Y la toa do di den cua quan co doi phuong,
  Qc la loai quan co di den }
Var OpenX, OpenY : Integer;

    WindBuffer : Pointer;
    WindSize : Word;
    Mx, My, LastMx, LastMy : Integer;

Begin
     DangMo := False;
     If CoDoiphuongDiden(X,Y,Qc) and Ganhduoc(X,Y,Qc) then
     Begin
          If X < 5 then
          Begin
               GetToadoThuc(X,Y,OpenX,OpenY);
               SaveWind(OpenX,OpenY,OpenX + 140,OpenY + 50,WindBuffer,WindSize);
          End
          Else
          Begin
               GetToadoThuc(X-2,Y,OpenX,OpenY);
               SaveWind(OpenX + 20,OpenY,OpenX + 160,OpenY + 50,WindBuffer,WindSize);
          End;
          For i:= 1 to 3 do
          Begin
               If i < 3 then
               Begin
                    If X < 5 then
                        PutImage(OpenX,OpenY,OpenPtrRight^,CopyPut)
                    Else
                        PutImage(OpenX + 20,OpenY,OpenPtrLeft^,CopyPut);
                    Delay(50);
                    If X < 5 then
                    Begin
                         RestorWind(OpenX,OpenY,WindBuffer,WindSize);
                         SaveWind(OpenX,OpenY,OpenX + 140,OpenY + 50,WindBuffer,WindSize);
                    End
                    Else
                    Begin
                         RestorWind(OpenX + 20,OpenY,WindBuffer,WindSize);
                         SaveWind(OpenX + 20,OpenY,OpenX + 160,OpenY + 50,WindBuffer,WindSize);
                    End;
                    Delay(50);
               End
               Else
                   If X < 5 then
                        PutImage(OpenX,OpenY,OpenPtrRight^,CopyPut)
                   Else
                        PutImage(OpenX + 20,OpenY,OpenPtrLeft^,CopyPut);
          End;
          Mouse.Show;
          Mouse.GetPos(Mx,My);
          LastMx := Mx; LastMy := My;
          Repeat
                Mouse.GetPos(Mx,My);
          Until (ABS(Mx - LastMx) > 15) or (ABS(My - LastMy) > 15);
          Mouse.Hide;
          If X < 5 then RestorWind(OpenX,OpenY,WindBuffer,WindSize)
          Else RestorWind(OpenX + 20,OpenY,WindBuffer,WindSize);
          Mouse.Show;
          DangMo := True;
     End;
End;
(*----------------------------------*)
Procedure Openning(X,Y : Integer; Qc : Byte);
{ X, Y la toa do di den cuar quan co doi phuong,
  Qc la loai quan co di den }
Var OpenX, OpenY : Integer;

    WindBuffer : Pointer;
    WindSize : Word;
    Mx, My, LastMx, LastMy : Integer;

Begin
     If CoDoiphuongDiden(X,Y,Qc) and Ganhduoc(X,Y,Qc) then
     Begin
          If X < 5 then
          Begin
               GetToadoThuc(X,Y,OpenX,OpenY);
               SaveWind(OpenX,OpenY,OpenX + 140,OpenY + 50,WindBuffer,WindSize);
          End
          Else
          Begin
               GetToadoThuc(X-2,Y,OpenX,OpenY);
               SaveWind(OpenX + 20,OpenY,OpenX + 160,OpenY + 50,WindBuffer,WindSize);
          End;
          For i:= 1 to 3 do
          Begin
               If i < 3 then
               Begin
                    If X < 5 then
                        PutImage(OpenX,OpenY,OpenningPtrRight^,CopyPut)
                    Else
                        PutImage(OpenX + 20,OpenY,OpenningPtrLeft^,CopyPut);
                    Delay(50);
                    If X < 5 then
                    Begin
                         RestorWind(OpenX,OpenY,WindBuffer,WindSize);
                         SaveWind(OpenX,OpenY,OpenX + 140,OpenY + 50,WindBuffer,WindSize);
                    End
                    Else
                    Begin
                         RestorWind(OpenX + 20,OpenY,WindBuffer,WindSize);
                         SaveWind(OpenX + 20,OpenY,OpenX + 160,OpenY + 50,WindBuffer,WindSize);
                    End;
                    Delay(50);
               End
               Else
                   If X < 5 then
                        PutImage(OpenX,OpenY,OpenningPtrRight^,CopyPut)
                   Else
                        PutImage(OpenX + 20,OpenY,OpenningPtrLeft^,CopyPut);
          End;
          Mouse.Show;
          Mouse.GetPos(Mx,My);
          LastMx := Mx; LastMy := My;
          Repeat
                Mouse.GetPos(Mx,My);
          Until (ABS(Mx - LastMx) > 15) or (ABS(My - LastMy) > 15);
          Mouse.Hide;
          If X < 5 then RestorWind(OpenX,OpenY,WindBuffer,WindSize)
          Else RestorWind(OpenX + 20,OpenY,WindBuffer,WindSize);
          Mouse.Show;
     End;
End;

(*----------------------------------*)
Procedure LamviecvoiMenu;
Var OldPattern : FillPatternType;
    Ch : Char;
Begin

     GetFillPattern(OldPattern);
     Repeat
           Mouse.GetPos(x,y);
           If RangeMenu(x,y) then ActiMenu(x,y);
     Until Not RangeMenu(x,y) Or (MenuSele <> 0);
     If MenuSele = 1 then
     Begin
           MenuSele := 0;
           ChuanbiBanco;
           Mouse.Show;
           Mouse.Show;
     End;
     If MenuSele = 2 then
     Begin
           MenuSele := 0;
           ActiLoad(SelectFile);
           Mouse.Show;
           Mouse.Show;
     End;
     If MenuSele = 3 then
     Begin
           MenuSele := 0;
           SaveGame(FileNameSave, FilePosSave);
           Mouse.Show;
           Mouse.Show;
     End;
     If MenuSele = 4 then
     Begin
           MenuSele := 0;
           StartX := 60;
           StartY := 100;
           DisplayScreen('HD.TXT');
           If Mouse.NotRightClick then Ch := Readkey;
           SetFillPattern(OldPattern,1);
           Bar(40,80,620,460);
           ReturnGame;
           Mouse.Show;
           Mouse.Show;
     End;
End;
(*----------------------------------*)
Procedure XuLyDiBangChuot;
Var StX, StY, StQc, StrNab,StrC : String;
Begin

     GetToadoLogic(x,y,ToadoLogic);

     If (Quanco[ToadoLogic.X,ToadoLogic.Y].Enable) and
        (ToadoLogic.X > 0) and (ToadoLogic.Y > 0) and
        (Quanco[ToadoLogic.X,ToadoLogic.Y].QC = QCActi) then
     Begin
          Mouse.Hide;
          If Not EnableMove then GetMove(LastX,LastY);
          LastX := ToadoLogic.X;
          LastY := ToadoLogic.Y;
          OddClick := True;
          GetMove(ToadoLogic.X,ToadoLogic.Y);
          EnableMove := False;
          Quanco[ToadoLogic.X,ToadoLogic.Y].Acti := True;
          Mouse.Show;
     End
     Else
     Begin
          If (ToadoLogic.X > 0) and (ToadoLogic.Y > 0) and OddClick and
             (Quanco[ToadoLogic.X,ToadoLogic.Y].Enable = False) and
             (ABS(ToadoLogic.X - LastX) <= 1) and
             (ABS(ToadoLogic.Y - LastY) <= 1) then
          Begin
               If (ABS(ToadoLogic.X - LastX) = 1) and
                  (ABS(ToadoLogic.Y - LastY) = 1) and
                  Odd(LastX + LastY) then
               Else
               Begin
                    If DangMo and
                       ((ToadoLogic.X <> OpenX) or (ToadoLogic.Y <> OpenY)) then
                    Begin
                         Write(#7);
                         Sound(500);
                         Delay(100);
                         NoSound;
                         Mouse.Hide;
                         Openning(OpenX, OpenY, QcActi);
                         Mouse.Show;
                         Exit;
                    End;
                    DangMo := False; { Xoa co Dang mo de tiep tuc di }
                    Mouse.Hide;
                    PhucHoiDinh(LastX,LastY);
                    Quanco[LastX,LastY].Enable := False;
                    Quanco[LastX,LastY].QC := 9;
                    Quanco[ToadoLogic.X,ToadoLogic.Y].Color := Quanco[LastX,LastY].Color;
                    Quanco[ToadoLogic.X,ToadoLogic.Y].QC := QcActi;
                    Quanco[ToadoLogic.X,ToadoLogic.Y].Enable := True;
                    Quanco[ToadoLogic.X,ToadoLogic.Y].X := ToadoLogic.X;
                    Quanco[ToadoLogic.X,ToadoLogic.Y].Y := ToadoLogic.Y;
                    VeQuanco(ToadoLogic.X, ToadoLogic.Y, Quanco[ToadoLogic.X,ToadoLogic.Y].Color);
                    XulyGanh(Quanco[ToadoLogic.X,ToadoLogic.Y]);
                    OddClick := False;
                    EnableMove := True;
                    Quanco[LastX,LastY].Acti := False;
                    Inc(QcActi);
                    If QcActi > 2 then QcActi := 1;
                    KiemtraBiduong(QcActi);
                    If Not Coganh and Open then
                    Begin
                         ShowOpen(LastX, LastY, QcActi);
                         OpenX := LastX;
                         OpenY := LastY;
                    End;
                    If Open then
                    Begin
                         Open := False;
                         ActiWind;
                    End;
                    Mouse.Show;
               End;
          End;
     End;
     Repeat Until Mouse.NotLeftClick;
End;
(*--------------------------------------*)
BEGIN
     KhoidongHethong;
     ChuanbiBanco;
     InitializeGame;
     Mouse.Show;
     LastX := 1; LastY := 1;
     OddClick := False;
     EnableMove := True;
     QCActi := 1;
     Nguoichoi := False;
     Mouse.Show;
     Open := False;
     ActiWind;
     Repeat
           While Not KeyPressed do
           Begin
                Mouse.GetPos(x,y);
                If RangeWind(x,y) then ActiWind;
                If RangeMenu(x,y) then LamviecvoiMenu
                Else
                    If Mouse.LeftClick then XuLyDiBangChuot;
                If MenuSele = 5 then
                Begin
                     CloseProgram;
                     CloseGraph;
                     Exit;
                End;
           End;
           Ch := ReadKey;
     Until Ch = #27;
     CloseProgram;
     CloseGraph;
END.
