class TrajectoryGenerator:
    def __init__(self, max_speed, acc_time, exec_frequency=10):
        self.max_speed = max_speed
        self.exec_frequency = exec_frequency
        self.initional_position = int(0)
        self.current_position = int(0)
        self.current_velocity = int(0)
        self.target_position = int(0)
        self.remainder_vel = 0.0
        self.req_velocity = 0.0
        self.cmd_velocity = 0.0
        self.acc = 0.0
        self.dis_con = int(0) # distance to constant speed
        self.reached = False
        self.shape = False # False: triangle, True: trapezoid
        self.acc_time = acc_time
        self.constant_speed_time = int(0)
        self.exec_time = int(0)

    def set_max_speed(self, max_speed):
        self.max_speed = max_speed

    def set_acc_time(self, acc_time):
        self.acc_time = acc_time

    def set_exec_frequency(self, exec_frequency):
        self.exec_frequency = exec_frequency

    def set_initial_position(self, initial_position):
        self.initial_position = initial_position
        self.current_position = initial_position

    def set_target_position(self, target_position):
        self.target_position = target_position
        tot_dis = self.target_position - self.initial_position
        dis_acc_dec = self.max_speed * self.acc_time
        if abs(tot_dis) < dis_acc_dec:
            self.req_velocity = abs(tot_dis) / self.acc_time # adjust the max speed
            dis_acc_dec = self.req_velocity* self.acc_time # adjust the distance to reach the max speed
            self.shape = False # triangle
        else:
            self.req_velocity = self.max_speed
            self.shape = True # trapezoid

        self.dis_con = abs(tot_dis) - dis_acc_dec # distance to constant speed
        self.acc = self.req_velocity/self.acc_time # acceleration and deceleration
        self.remainder_vel = 0.0 # remainder velocity
        self.constant_speed_time = int(self.dis_con/self.req_velocity) # time to keep the constant speed
        self.cmd_velocity = 0.0 # command velocity

    def execute(self):
        # check if the distance is long enough to reach the max speed.
        # if not, the speed should be adjusted to reach the target position
        # within the acc_time.
        # And there are two shape whitch is triangle and trapezoid.        
        distance = self.target_position - self.current_position
        self.exec_time += 1
        if self.shape == False:
            if self.exec_time <= self.acc_time:
                self.cmd_velocity = self.cmd_velocity + self.acc
            else:
                if self.exec_time == (self.acc_time + self.acc_time):
                    self.cmd_velocity = distance
                    self.remainder_vel = 0.0
                else:
                    self.cmd_velocity = self.cmd_velocity - self.acc
        else: # trapezoid
            if self.exec_time <= self.acc_time:
                self.cmd_velocity = self.cmd_velocity + self.acc
            elif self.acc_time < self.exec_time <= (self.constant_speed_time + self.acc_time):
                self.cmd_velocity = self.req_velocity
            else:
                if self.exec_time == (self.constant_speed_time + self.acc_time + self.acc_time):
                    self.cmd_velocity = distance
                    self.remainder_vel = 0.0
                else:
                    self.cmd_velocity = self.cmd_velocity - self.acc

        # else:
        #     self.reached = False
        #     direction = 1 if distance > 0 else -1
        #     self.current_velocity = min(self.max_speed, abs(distance) / self.acc_time) * direction
        #     self.current_position += self.current_velocity / self.exec_frequency

        self.current_velocity = int( self.cmd_velocity+0.5+self.remainder_vel)
        self.current_position += self.current_velocity
        self.remainder_vel = self.current_velocity - self.cmd_velocity

        if self.current_position == self.target_position:
            self.reached = True
        else:
            self.reached = False
            

        return self.reached

    def get_current_position(self):
        return self.current_position

    def get_current_velocity(self):
        return self.current_velocity

if __name__ == "__main__":
    max_speed = 100
    acc_time = 10
    exec_frequency = 10
    trj = TrajectoryGenerator(max_speed, acc_time, exec_frequency)
    trj.set_initial_position(0)
    trj.set_target_position(10)
    print("idx","pos", "vel")
    for i in range(100):
        trj.execute()
        print(i, trj.get_current_position(), trj.get_current_velocity())
        if trj.reached:
            break