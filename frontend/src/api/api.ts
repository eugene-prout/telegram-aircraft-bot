interface FlightRequest {
    latitude: number;
    longitude: number;
  }
  
  interface AircraftDescriptionRequest {
    aircraft_name: string;
  }
  
  interface FlightObservation {
    heading: number;
    origin: string;
    destination: string;
    relative_angle: number;
    ground_distance: number;
    aircraft: string;
    aircraft_latitude: number;
    aircraft_longitude: number;
    callsign: string;
    photo?: string | null;
  }
  
  interface FlightResponse {
    observations: FlightObservation[];
    radar_map: string;
  }
  
  async function getFlights(requestData: FlightRequest): Promise<FlightResponse> {
    const response = await fetch('/api/flights', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(requestData),
    });
  
    if (!response.ok) {
      throw new Error(`Failed to fetch flights: ${response.statusText}`);
    }
  
    return response.json();
  }
  
  async function getAircraftInformation(requestData: AircraftDescriptionRequest): Promise<FlightResponse> {
    const response = await fetch('/api/aircraft', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(requestData),
    });
  
    if (!response.ok) {
      throw new Error(`Failed to fetch aircraft information: ${response.statusText}`);
    }
  
    return response.json();
  }

export { type FlightRequest, type AircraftDescriptionRequest, type FlightObservation, getFlights, getAircraftInformation } 
