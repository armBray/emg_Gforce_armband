%%%%%%%%%%%%%%%%%%%%%%%%%%%
%   This function carries out two main functions
%       1 - Define and open the serial port
%       2 - Set Bracialet instruction
%       3 - Read pack data
%   Input:
%       1 - [scalar]	Acquisition's Phase [1,2,3]        
%		2 - [scalar]	Acquisition's frequency [100,500,650,1000]
%		3 - [scalar]	Acquisition's resolution [8bits , 12bits]
%		4 - [scalar]	Acquisition's channels [1,2,3,4,5,6,7,8]  
%	Output: 
%		1 - [column vector 141x1]   data pack w/o header
%
%   For any further information please read the <information_file> or contact
%       - Armando Amerì to armando.ameri@studio.unibo.it
%       - Roberto Meattini to roberto.meattini2@unibo.it
%%%%%%%%%%%%%%%%%%%%%%%%%%%

function [dati] = EMG_Raw_Data_Pack(u,freq,resolution,ch)

coder.extrinsic('serial', 'fopen','fprintf','instrfind','display','get','instrreset', 'run');

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

        s = serial('COM3','BaudRate',115200);
        %s = serial('COM4','BaudRate',115200);
        set(s,'InputBufferSize',10000000);
        %get(s,"BytesAvailable")
        fopen(s);
        
        %-------------------------------------%
        %--- SIMULINK -> Acquisition Phase ---%    
        %-------------------------------------% 
        if u==1
            %*** settings data sending ***%
            sEMG_settings(s,freq,resolution,ch,ch_mask);
            %*** starting exchange data command ***%
            %Old Bracialet
            txdata = ['01';'B6';'FD';'09';'00';'00';'1E';'00';'4F';'80';'00';'00';'00']; %13
            %New Bracialet
            %txdata = ['01';'B6';'FD';'09';'00';'00';'21';'00';'4F';'80';'00';'00';'00']; %13
            %Convert to decimal format
            txdata_dec = hex2dec(txdata);
            %Write using the UINT8 data format
            fwrite(s,txdata_dec,'uint8')
            scambio_dati = 1;
            disp('Avvio scambio'); 
            
            %*** OFFSET FIRST HEADER  ***%
            display('offset_header()')
            fread(s,3+6+3+10,'uint8')
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
    
    %---------------------------------------------------------%
    %--- read data pack (EMG HEADER [22] + EMG DATA [128]) ---%
    %---------------------------------------------------------%
    byte_eval = get(s,"BytesAvailable");
    if  scambio_dati 
        dati = zeros(141,1);
        dati = fread(s,141,'uint8');
        byte_eval = get(s,"BytesAvailable")
    else
        dati = zeros(141,1);
    end

end