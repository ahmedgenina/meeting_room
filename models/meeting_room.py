# -*- coding: utf-8 -*-
from dateutil.relativedelta import relativedelta
from odoo import api, fields, models, tools, _
from odoo.exceptions import UserError
from cookielib import vals_sorted_by_key

class MeetingRoom(models.Model):
  
    _name = 'meeting.room'
    _description = 'List available rooms'
    #_order = 'license_plate asc'

    name = fields.Char('Name', required=True , help='Name of the meeting room')
    location = fields.Char('Location', required=False , help='Location of the meeting room')
    capacity = fields.Integer('Seats Number', help='Number of seats of the room')
    active = fields.Boolean(default=True,help='Room available for reservations?')
    wifi =  fields.Boolean(default=False,help='wifi available?')
    AC =  fields.Boolean(default=False,help='Air condition available?')
    printer =  fields.Boolean(default=False,help='Printer available?')
    projector =  fields.Boolean(default=False,help='Projector available?')

class Reservations(models.Model):

    _name = 'meeting.reservation'
    _description = 'List available reservations'
    #_order = 'reservation_date '

    periods = [('6.5','6:30'),('7','7:00'),
    ('7.5','7:30'),('8','8:00'),
    ('8.5','8:30'),('9','9:00'),
    ('9.5','9:30'),('10','10:00'),
    ('10.5','10:30'),('11','11:00'),
    ('11.5','11:30'),('12','12:00'),
    ('12.5','12:30'),('13','13:00'),
    ('13.5','13:30'),('14','14:00'),
    ('14.5','14:30'),('15','15:00'),
    ('15.5','15:30'),('16','16:00'),
    ('16.5','16:30'),('17','17:00'),
    ('17.5','17:30'),('18','18:00'),
    ('18.5','18:30'),('19','19:00'),    
    ('19.5','19:30'),('20','20:00')]
    
    room_id = fields.Many2one('meeting.room','Room')
    reservation_date= fields.Date('Reservation date' , required=True,help='Date when the room to be reserved')
    user_id = fields.Many2one('res.users', 'Responsible')
    start_time = fields.Selection(periods,string='Start Time',help='Time for the meeting to start')
    end_time = fields.Selection(periods,string='End Time',help='Time for the meeting to end')
    
    @api.model
    def create(self,vals):
      #  import pdp; pdp.set_trace() 
        new_record = super(Reservations,self).create(vals)        
        return new_record
    
    
    @api.multi
    def write(self,vals):
    
        super(Reservations, self).write(vals)
        return True




























# RST = requested start time
# RET = requested end tim
# reserved  >       10 |---------------------|12 (min_start)                                16|---------------|19 (other)  

#room 1 8|----10|  12|---------16|  
#room 2 
# required  >                                                      14|----------------------------------|18 (min_start)
#dic = from reservations select * where date = required_date and room = room_id
#for rec in dic :
#    if (RST >= startime and RST < endtime ) or (RET > starttime and RET <= entime):
#        return occupied  

# min_start = required if required.start_time<reserved.start_time else reserved
# other = required if min_start==reserved else reserved
# return 'occupied' if   other.start_time<min_start.end_time else 'free'

#starttime 10
#endtime 12


#8-10  ok
#8-11  no
#11-15 no
#13-18 ok



"""

    company_id = fields.Many2one('res.company', 'Company')
    license_plate = fields.Char(required=True, help='License plate number of the vehicle (i = plate number for a car)')
    vin_sn = fields.Char('Chassis Number', help='Unique number written on the vehicle motor (VIN/SN number)', copy=False)
    driver_id = fields.Many2one('res.partner', 'Driver', help='Driver of the vehicle')
    model_id = fields.Many2one('fleet.vehicle.model', 'Model', required=True, help='Model of the vehicle')
    log_fuel = fields.One2many('fleet.vehicle.log.fuel', 'vehicle_id', 'Fuel Logs')
    log_services = fields.One2many('fleet.vehicle.log.services', 'vehicle_id', 'Services Logs')
    log_contracts = fields.One2many('fleet.vehicle.log.contract', 'vehicle_id', 'Contracts')
    cost_count = fields.Integer(compute="_compute_count_all", string="Costs")
    contract_count = fields.Integer(compute="_compute_count_all", string='Contracts')
    service_count = fields.Integer(compute="_compute_count_all", string='Services')
    fuel_logs_count = fields.Integer(compute="_compute_count_all", string='Fuel Logs')
    odometer_count = fields.Integer(compute="_compute_count_all", string='Odometer')
    acquisition_date = fields.Date('Acquisition Date', required=False, help='Date when the vehicle has been bought')
    color = fields.Char(help='Color of the vehicle')
    state_id = fields.Many2one('fleet.vehicle.state', 'State', default=_get_default_state, help='Current state of the vehicle', ondelete="set null")
    location = fields.Char(help='Location of the vehicle (garage, ...)')
    seats = fields.Integer('Seats Number', help='Number of seats of the vehicle')
    doors = fields.Integer('Doors Number', help='Number of doors of the vehicle', default=5)
    tag_ids = fields.Many2many('fleet.vehicle.tag', 'fleet_vehicle_vehicle_tag_rel', 'vehicle_tag_id', 'tag_id', 'Tags', copy=False)
    odometer = fields.Float(compute='_get_odometer', inverse='_set_odometer', string='Last Odometer', help='Odometer measure of the vehicle at the moment of this log')
    odometer_unit = fields.Selection([('kilometers', 'Kilometers'), ('miles', 'Miles')],
        'Odometer Unit', default='kilometers', help='Unit of the odometer ', required=True)
    transmission = fields.Selection([('manual', 'Manual'), ('automatic', 'Automatic')], 'Transmission', help='Transmission Used by the vehicle')
    fuel_type = fields.Selection([('gasoline', 'Gasoline'), ('diesel', 'Diesel'), ('electric', 'Electric'), ('hybrid', 'Hybrid')], 'Fuel Type', help='Fuel Used by the vehicle')
    horsepower = fields.Integer()
    horsepower_tax = fields.Float('Horsepower Taxation')
    power = fields.Integer('Power', help='Power in kW of the vehicle')
    co2 = fields.Float('CO2 Emissions', help='CO2 emissions of the vehicle')
    image = fields.Binary(related='model_id.image', string="Logo")
    image_medium = fields.Binary(related='model_id.image_medium', string="Logo (medium)")
    image_small = fields.Binary(related='model_id.image_small', string="Logo (small)")
    contract_renewal_due_soon = fields.Boolean(compute='_compute_contract_reminder', search='_search_contract_renewal_due_soon', string='Has Contracts to renew', multi='contract_info')
    contract_renewal_overdue = fields.Boolean(compute='_compute_contract_reminder', search='_search_get_overdue_contract_reminder', string='Has Contracts Overdue', multi='contract_info')
    contract_renewal_name = fields.Text(compute='_compute_contract_reminder', string='Name of contract to renew soon', multi='contract_info')
    contract_renewal_total = fields.Text(compute='_compute_contract_reminder', string='Total of contracts due or overdue minus one', multi='contract_info')
    car_value = fields.Float(help='Value of the bought vehicle')

"""