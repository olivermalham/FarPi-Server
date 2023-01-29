import serial


class GPSPacket:

    # Packet parameters
    packet_type = None
    time = None                     # HHmmss
    latitude = None                 # dddmm.mmmm
    latitude_hemisphere = None      # N or S
    longitude = None                # dddmm.mmmm
    longitude_hemisphere = None     # W or E
    gps_fix = None                  # 0 = invalid, 1 = GPS fix, 2 = DGPS fix
    number_satellites = None        # satellites in view
    hdop = None                     # Relative accuracy of horizontal position
    altitude = None                 # meters
    altitude_units = None           # 'M' = meters
    geoid_wgs84 = None              # meters
    geoid_wgs84_units = None        # 'M' = meters
    time_since_dgps_update = None
    dgps_ref_station_id = None
    checksum = None
    ns_indicator = None
    ew_indicator = None
    utc_time = None
    status = None
    mode = None

    @staticmethod
    def new(gps_data):
        gps_data = gps_data.strip()
        if gps_data is None or gps_data == b'':
            return None
        sentence_parts = gps_data.split(b",")
        data_checksum = sentence_parts[-1].split(b"*")
        sentence_parts[-1] = data_checksum[0]
        sentence_parts.append(data_checksum[1])
        sentence_type = sentence_parts[0][1:]

        if len(sentence_type) == 0:
            return None

        if sentence_type == b"GPGGA":
            return GPSPacket.gpgga(sentence_parts[1:])

        if sentence_type == b"GPGLL":
            return GPSPacket.gpgll(sentence_parts[1:])

        if sentence_type == b"GPVTG":
            return GPSPacket.gpvtg(sentence_parts[1:])

        if sentence_type == b"GPRMC":
            return GPSPacket.gprmc(sentence_parts[1:])

        if sentence_type == b"gpgsa":
            return GPSPacket.gpgsa(sentence_parts[1:])

        # Disabling for now, not sure how much I care about "satellites in view" data
        # if sentence_type == b"GPGSV":
        #     return GPSPacket.GPGSV(sentence_parts[1:])

        # Informational only I think, not really interested
        # if sentence_type == b"gptxt":
        #     return GPSPacket.GPTXT(sentence_parts[1:])

    @staticmethod
    def gpgga(params):
        """
        Global positioning system fix data (time, position, fix type data)
        :param params:
        :return:
        """
        if len(params) < 15:
            print(f"GPGGA Malformed - {len(params)}: {params}")
            return None

        new_packet = GPSPacket()
        new_packet.time = params[0]
        new_packet.latitude = float(params[1][:2]) + float(params[1][2:])/60 if params[1] != b'' else None
        new_packet.latitude_hemisphere = params[2]
        new_packet.longitude = float(params[3][:3]) + float(params[3][3:])/60 if params[3] != b'' else None
        new_packet.longitude_hemisphere = params[4]
        new_packet.gps_fix = params[5]
        new_packet.number_satellites = params[6]
        new_packet.hdop = params[7]
        new_packet.altitude = params[8]
        new_packet.altitude_units = params[9]
        new_packet.geoid_wgs84 = params[10]
        new_packet.geoid_wgs84_units = params[11]
        new_packet.time_since_dgps_update = params[12]
        new_packet.dgps_ref_station_id = params[13]
        new_packet.checksum = params[14]
        new_packet.packet_type = "GPGGA"

        return new_packet

    @staticmethod
    def gpgll(params):
        """
        Geographic position, latitude, longitude
        :param params:
        :return:
        """
        if len(params) < 8:
            print(f"GPGLL Malformed - {len(params)}: {params}")
            return None

        new_packet = GPSPacket()
        new_packet.latitude = params[0]
        new_packet.ns_indicator = params[1]
        new_packet.longitude = params[2]
        new_packet.ew_indicator = params[3]
        new_packet.utc_time = params[4]
        new_packet.status = params[5]
        new_packet.mode = params[6]
        new_packet.checksum = params[7]
        new_packet.packet_type = "GPGLL"

        return new_packet

    @staticmethod
    def gpvtg(params):
        """
        Course and speed information relative to the ground
        :param params:
        :return:
        """
        if len(params) < 10:
            print(f"GPVTG Malformed - {len(params)}: {params}")
            return None

        new_packet = GPSPacket()
        new_packet.course = params[0]
        new_packet.reference = params[1]
        new_packet.course = params[2]
        new_packet.reference = params[3]
        new_packet.speed = params[4]
        new_packet.units = params[5]
        new_packet.speed = params[6]
        new_packet.units = params[7]
        new_packet.mode = params[8]
        new_packet.checksum = params[9]
        new_packet.packet_type = "GPVTG"

        return new_packet

    @staticmethod
    def gprmc(params):
        """
        Time, date, position, course, and speed data
        :param params:
        :return:
        """
        if len(params) < 12:
            print(f"GPRMC Malformed - {type(params)}: {params}")
            return None

        new_packet = GPSPacket()
        new_packet.utc_time = params[0]
        new_packet.status = params[1]
        new_packet.latitude = params[2]
        new_packet.ns_indicator = params[3]
        new_packet.longitude = params[4]
        new_packet.ew_indicator = params[5]
        new_packet.speed = params[6]
        new_packet.course = params[7]
        new_packet.date = params[8]
        new_packet.magnetic_variation = params[9]
        new_packet.mode = params[10]
        new_packet.checksum = params[11]
        new_packet.packet_type = "GPRMC"

        return new_packet

    @staticmethod
    def gpgsa(params):
        """
        GPS receiver operating mode, satellites used in the position solution, and DOP values.
        :param params:
        :return:
        """
        if len(params) < 17:
            print(f"GPGSA Malformed - {len(params)}: {params}")
            return None

        new_packet = GPSPacket()
        new_packet.mode = params[0]
        new_packet.fix_quality = params[1]
        new_packet.prn = params[2:13]
        new_packet.pdop = params[14]
        new_packet.hdop = params[15]
        new_packet.vdop = params[16]
        new_packet.packet_type = "GPGSA"

        return new_packet

    @staticmethod
    def gpgsv(params):
        """
        The number of GPS satellites in view, satellite ID numbers, elevation, azimuth, and SNR values.
        :param params:
        :return:
        """
        if len(params) < 13:
            print(f"GPGSV Malformed - {len(params)}: {params}")
            return None

        new_packet = GPSPacket()
        new_packet.time = params[0]
        new_packet.latitude = params[1]
        new_packet.latitude_hemisphere = params[2]
        new_packet.gps_fix = params[3]
        new_packet.number_satellites = params[4]
        new_packet.hdop = params[5]
        new_packet.altitude = params[6]
        new_packet.altitude_units = params[7]
        new_packet.geoid_wgs84 = params[8]
        new_packet.geoid_wgs84_units = params[9]
        new_packet.time_since_dgps_update = params[10]
        new_packet.dgps_ref_station_id = params[11]
        new_packet.checksum = params[12]
        new_packet.packet_type = "GPGSV"

        return new_packet
    #
    # @staticmethod
    # def gptxt(params):
    #     """
    #     Informational text?
    #     :param params:
    #     :return:
    #     """
    #     return None  # For now ignore
    
    def __repr__(self):
        result = ""
        result = result + f"Type: {self.packet_type}\n"
        result = result + f"time: {self.time}\n"
        result = result + f"latitude: {self.latitude}\n"
        result = result + f"latitude_hemisphere: {self.latitude_hemisphere}\n"
        result = result + f"longitude: {self.longitude}\n"
        result = result + f"longitude_hemisphere: {self.longitude_hemisphere}\n"
        result = result + f"gps_fix: {self.gps_fix}\n"
        result = result + f"number_satellites: {self.number_satellites}\n"
        result = result + f"hdop: {self.hdop}\n"
        result = result + f"altitude: {self.altitude}\n"
        result = result + f"altitude_units: {self.altitude_units}\n"
        result = result + f"geoid_wgs84: {self.geoid_wgs84}\n"
        result = result + f"geoid_wgs84_units: {self.geoid_wgs84_units}\n"
        result = result + f"time_since_dgps_update: {self.time_since_dgps_update}\n"
        result = result + f"dgps_ref_station_id: {self.dgps_ref_station_id}\n"
        result = result + f"checksum: {self.checksum}\n"
        result = result + f"ns_indicator: {self.ns_indicator}\n"
        result = result + f"ew_indicator: {self.ew_indicator}\n"
        result = result + f"utc_time: {self.utc_time}\n"
        result = result + f"status: {self.status}\n"
        result = result + f"mode: {self.mode}\n"
        return result


if __name__ == "__main__":
    GPS_SERIAL_PORT = "/dev/ttyACM0"
    gps_serial = serial.Serial(GPS_SERIAL_PORT, 115200, timeout=0.2)

    while True:
        data = gps_serial.readline()

        # print(f"Data Packet: {data_parts}; Checksum: {data_checksum}")
        packet = GPSPacket.new(data)
        if packet is not None and packet.packet_type == "GPGGA":
            print(f"Packet processed: {packet}")
