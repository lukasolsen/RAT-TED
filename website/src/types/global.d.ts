type Victims = {
  uuid: string;
  name: string;
  ip: string;
  status: string;
};

type Victim = {
  architecture: string;
  city: string;
  computer_name: string;
  connection_type: string;
  country: string;
  id: number;
  ip: string;
  isp: string;
  latitude: string;
  longitude: string;
  organization: string;
  os: string;
  postal: string;
  region: string;
  region_name: string;
  screen_share_source: string;
  socket_ip: string;
  status: string;
  timezone: string;
  username: string;
};

type CommandResultType = {
  result: string;
  error: string;
};
