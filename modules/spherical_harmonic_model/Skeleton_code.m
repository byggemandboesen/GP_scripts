%% Skeletal code
close all; clc; clear all;
g_coeff = load('g_coefficients.txt');
h_coeff = load('h_coefficients.txt');

%%
lat = (1:1:179); % In colatitude
lon = (-180:2:180);
nlat = length(lat);
nlon = length(lon);
lat = repmat(lat',[1,nlon]); %Create meshgrid
lon = repmat(lon,[nlat,1]); % Create meshgrid
r = 6378000;
a = 6378000;
n_max = 13;

lon = lon * pi/180;
lat = lat * pi/180;

val = zeros(nlat,nlon); % This should be your grid with radial component.

%-----------------------------------------------------------------
% Insert your code here to evaluate the radial component from the spherical
% harmonic coefficients. 
% hint for legendre : P = legendre(n,cos(lat)),'sch'); creates legendre pol
% for deg n, at colatitude lat.
% Some loops would be a good idea. What should we loop over?

%-----------------------------------------------------------------

%% Plotting
% Set parameters for plotting
load('world.mat')
ptype      = 'grid';                   % Type of input, can be 'grid' or 'points'
icoastline = 'world.mat';            % Coast line to be used, can be 'dummy'
x          = lon*180/pi;             % X or longitude coordinates
y          = lat*180/pi - 90;                % Y or latitude coordinates (NOT colatitude)
value      = 0;% INSERT VALUE                % Value to be plotted with colorscale                
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