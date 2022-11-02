%% Skeletal code
close all; clc; clear all;
g_coeff = load('g_coefficients.txt');
h_coeff = load('h_coefficients.txt');

%%
lat = (-89:1:89);
lon = (-180:2:180);
nlat = length(lat);
nlon = length(lon);
lat = repmat(lat',[1,nlon]);
lon = repmat(lon,[nlat,1]);
r = 6378000;
a = 6378000;
n_max = 13;

lon = lon * pi/180;
lat = lat * pi/180;

val = zeros(nlat,nlon);

% Loop over latitude
for i = 1:nlat
% Loop over degree
    for n = 0:n_max
        term = zeros(1,nlon);
        P = legendre(n,cos(lat(i,1)+90*pi/180),'sch');
% Loop over order
        for m = 0:n
            term = term + P(m+1) * (g_coeff(n+1,m+1)*cos(m*lon(i,:))+ h_coeff(n+1,m+1)*sin(m*lon(i,:)));
        end
% Account for degree dependent factor, e.g.
        val(i,:) = val(i,:) + term * (n+1)*((a/r)^(n+2));
    end
end

%% Plotting
% Set parameters for plotting
load('world.mat')
ptype      = 'grid';                   % Type of input, can be 'grid' or 'points'
icoastline = 'world.mat';            % Coast line to be used, can be 'dummy'
x          = lon*180/pi;                % X or longitude coordinates
y          = lat*180/pi;                   % Y or latitude coordinates (NOT colatitude)
value      = flip(val);                 % Value to be plotted with colorscale                
ftitle     = 'Radial magnetic field component of internal sources';          % Figure title
cbtitle    = 'Field [nT]';  % Label on colorbar
cbval      = inf;                      % Colobar limits, Inf for automatic
cbmap      = 'jet';                    % Colormap used, can be 'dem' or 'dummy'
fpos       = [50 50 1000 700];          % Figure position, Inf for default
x_lim      = [min(min(x)),max(max(x))];               % x-axis limits, Inf for automatic
y_lim      = [min(min(y)),max(max(y))];                  % y-axis limits, Inf for automatic
fxlabel    = 'Longitude [deg]';        % Label on x-axis, can be 'none'
fylabel    = 'Latitutde [deg]';        % Label on y-axis, can be 'none'

% Call plotting routine
% plotting function:
% Credit to Tim Enzlberger Jensen, DTU SPACE
plot_data(ptype,icoastline,x,y,value,ftitle,cbtitle,cbval,cbmap,fpos,x_lim,y_lim,fxlabel,fylabel);