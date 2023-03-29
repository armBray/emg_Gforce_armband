%% Inizialization
M_pinv = zeros(2,8);
k_ext = 1;
k_flex = 1;

%% Plot
% load('calibration_New');

plot(previousSession.emg_rms.Data)
A = previousSession.emg_rms.Data';

%% Range
range = [79642;92017;89500;90100]; % [extreme_left_total_signal extreme_right_total_signal extreme_left_stiff extreme_right_stiff]
diff_range = range(2,1)-range(1,1);
diff_range_2 = range(4,1)-range(3,1);

%% Computation
[M,U_Offline] = nnmf(A(:,range(1,1):range(2,1)),2);
plot(U_Offline')
M_pinv = pinv(M);

s_ext = M(:,1);
s_flex = M(:,2);

u_ext = U_Offline(1,:)';
u_flex = U_Offline(2,:)';

k_ext = sum(u_ext)/diff_range_2;
k_flex = sum(u_flex)/diff_range_2;

%% Online

U_Online = M_pinv*previousSession.emg_rms.Data';
a_ext = U_Online(1,:)'/k_ext;
a_flex = U_Online(2,:)'/k_flex;
a = [a_ext;a_flex];
cc_level = min(a_ext,a_flex);
plot(cc_level)

%% Plot finale
% plot(normalize(previousSession.cc_gamma.Data,'range'))
plot(normalize(cc_level,'range'))
