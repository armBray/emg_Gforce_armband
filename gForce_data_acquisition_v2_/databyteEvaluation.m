% **************************************************************************************************************
% Created on Tue Sept 20 2022
% @autor: Armando Amerì
% @e-mail: armando.ameri@studio.unibo.it
% @description:   matlabScript that makes a bytes evaluation based on datas that you want to read on COM port.
%                 Values to be settled:
%                 - COM
%                 - BAUDRATE
% **************************************************************************************************************

%--------------------
% Settaggio parametri
%--------------------
bracialet = string(input("Which bracialet are you using? Set 1 for Old or 2 for New:   "));

if bracialet == "1"
    bracialetByte = '1E';
else
    bracialetByte = '21';
end

freq = 1000;
resolution = 8;
ch = 8;
ch_mask='FF';
a=true;
do_write = false;

%***************************%
%*** Serial port opening ***%  
%***************************%
fprintf('sono dentro isempty\n');     
a=isempty(instrfind);
if a==0
    fclose(instrfind);
end

s = serial('COM4','BaudRate',115200);
% s = serial('COM41','BaudRate',115200);
set(s,'InputBufferSize',100000);
fopen(s);


%--------------------
% MENU Visualization
%--------------------
fprintf("What datas do you want to evaluate?\n")
fprintf("Please digit:\n")
fprintf("01 Acceleration\n")
fprintf("02 Gyroscope\n")
fprintf("04 Magnetometer\n")
fprintf("08 Euler Angle\n")         %ok
fprintf("10 Quaternion\n")          %ok
fprintf("20 Rotation Matrix\n")     %ok
fprintf("80 EMG\n")                 %ok
fprintf("88 EMG + Euler Angle\n")   %ok
fprintf("90 EMG + Quaternion\n")    %ok
dataReq = string(input("Input:   "))

if strlength(dataReq) == 1
    dataReq = "0" + dataReq;
end

%****************************%
%*** settaggio invio dati ***%
%****************************%
if dataReq == "08" || dataReq == "10"
    txdata = ['01';'92';'FD';'09';'00';'00';bracialetByte;'00';'4F';dataReq;'00';'00';'00'];
    do_write = true;
elseif dataReq == "20" 
    txdata = ['01';'82';'FD';'04';'00';'00';'29';'00'];
    %Convert to decimal format
    txdata_dec = hex2dec(txdata);
    %Write using the UINT8 data format
    fwrite(s,txdata_dec,'uint8');
    pause(15);
    txdata = ['01';'92';'FD';'09';'00';'00';bracialetByte;'00';'4F';dataReq;'00';'00';'00'];
    do_write = true;
elseif dataReq == "80"
    sEMG_settings(s,freq,resolution,ch,'FF');
    txdata = ['01';'B6';'FD';'09';'00';'00';bracialetByte;'00';'4F';dataReq;'00';'00';'00'];
    do_write = true;
elseif dataReq == "88"
    sEMG_settings(s,freq,resolution,ch,'FF');
    txdata = ['01';'92';'FD';'09';'00';'00';bracialetByte;'00';'4F';dataReq;'00';'00';'00'];
    do_write = true;
elseif dataReq == "90"
    sEMG_settings(s,freq,resolution,ch,'FF');
    txdata = ['01';'B6';'FD';'09';'00';'00';bracialetByte;'00';'4F';dataReq;'00';'00';'00'];
    do_write = true;
else
    fprintf("not already checked!\n")
end   

if do_write
    %Convert to decimal format
    txdata_dec = hex2dec(txdata);
    %Write using the UINT8 data format
    fwrite(s,txdata_dec,'uint8')
    fprintf('Avvio scambio');
    pause(10);
    byte_eval = get(s,"BytesAvailable")
    fread(s,byte_eval)
else
    fprintf("restart the script")
end


%% stop invio dati

txdata = ['01';'B6';'FD';'09';'00';'00';bracialetByte;'00';'4F';'00';'00';'00';'00']; %13
%Convert to decimal format
txdata_dec = hex2dec(txdata);
%Write using the UINT8 data format
fwrite(s,txdata_dec,'uint8')
fprintf('Stop scambio\n');
byte_eval = get(s,"BytesAvailable")

%--- flush dati rimanenti
while byte_eval
    flushinput(s);
    byte_eval = get(s,"BytesAvailable")
end

fprintf('Flush executed!');

fclose(s)
fprintf('Port closed\n');
delete(s)
fprintf('Port deleted\n');