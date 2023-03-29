%%%%%%%%%%%%%%%%%%%%%%%%%%%
%   This function carries out two main functions
%       1 - Define and open the serial port
%       2 - Set Bracialet instruction
%       3 - Read pack data
%   Input:  
%       1 - [scalar]	Acquisition's Phase [1,2,3] 
%		2 - [string]	Com Port 
%		3 - [string]	Hex of bracialet ID  
%	Output: 
%		1 - [column vector 141x1]   data pack w/o header
%
%   For any further information please read the <information_file> or contact
%       - Armando Amerì to armando.ameri@studio.unibo.it
%       - Roberto Meattini to roberto.meattini2@unibo.it
%%%%%%%%%%%%%%%%%%%%%%%%%%%

function [dati] = Data_Pack_rotation_matrix(u,comPort,bracialet)

coder.extrinsic('serial', 'fopen','fprintf','instrfind','display','get','instrreset', 'run','flushinput','assignin');

%-----------------------------%
%--- variables' definition ---%
%-----------------------------%
persistent scambio_dati
    if isempty(scambio_dati)
        scambio_dati = 0;
    end

persistent s
ch_mask='FF';
a=true;

    %-------------------------------------------------%
    %--- Serial port opening (if not already open) ---%    
    %-------------------------------------------------%    
    if isempty(s)
        disp('definizione porta seriale');     
        a=isempty(instrfind);

        if a==0
            fclose(instrfind);
        end

        bracialetByte = '';
        if bracialet == 0
            bracialetByte = '1E';
        else
            bracialetByte = '21';
        end  

        assignin('base','bracialetByte_var',bracialetByte);
        assignin('base','comPort_var',comPort);

        s = serial(comPort,'BaudRate',115200);
        set(s,'InputBufferSize',10000000);
        %get(s,"BytesAvailable")
        fopen(s);
  
        %-------------------------------------%
        %--- SIMULINK -> Acquisition Phase ---%    
        %-------------------------------------% 
        if u==1
            %*** starting exchange data command ***%
            txdata = ['01';'82';'FD';'04';'00';'00';'29';'00'];
            %Convert to decimal format
            txdata_dec = hex2dec(txdata);
            %Write using the UINT8 data format
            fwrite(s,txdata_dec,'uint8');
            pause(8);
            txdata = ['01';'92';'FD';'09';'00';'00';bracialetByte;'00';'4F';'20';'00';'00';'00']; %13
            %Convert to decimal format
            txdata_dec = hex2dec(txdata);
            %Write using the UINT8 data format
            fwrite(s,txdata_dec,'uint8')
            scambio_dati = 1;
            disp('Avvio scambio');
            
            %*** OFFSET HEADER  ***%
            display('offset_header()')
            fread(s,62,'uint8')
            display('offset_header ok')
        elseif u==2
            display('stop')
            run("stop_invio_dati_matlab.m")
            scambio_dati = 0;
        elseif u==3
            display('cc-level not already implemented!')
        else 
            display('others need to be implemented!')
        end
       
    end

    %-------------------------------------------------------------%
    %--- read data pack (EMG HEADER [13] + EMG DATA [9*long]) ----%
    %-------------------------------------------------------------% 
    if  scambio_dati 
        dati0 = zeros(13,1);
        dati0 = fread(s,13); 
        dati = zeros(9,1);
        dati = fread(s,9,'long'); % Rot[0][0], Rot[0][1], Rot[0][2], Rot[1][0],...
        byte_eval = get(s,"BytesAvailable")
    else
        dati = zeros(9,1);
    end

end