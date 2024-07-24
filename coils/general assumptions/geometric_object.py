import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
import math

class coil_geometry:
    '''geometric object'''
    def __init__(self, name):
        self.name = name

    def draw_coil(self):
        pass

class rund(coil_geometry):
    def __init__(self, name, winding_radius, inner_radius, number_of_windings_x, number_of_windings_y, spacing_between_windings):
        super().__init__(name)
        self.winding_radius = winding_radius
        self.inner_radius = inner_radius
        self.spacing_between_windings = spacing_between_windings
        self.number_of_windings_x = number_of_windings_x
        self.number_of_windings_y = number_of_windings_y
    
    @property
    def number_of_windings_total(self):
        return self.number_of_windings_x * self.number_of_windings_y

    @property
    def area_winding(self):
        return math.pi * self.winding_radius ** 2 - math.pi * self.inner_radius ** 2

    @property
    def len_x(self):
        return (self.spacing_between_windings + 2 * self.winding_radius) * self.number_of_windings_x + self.spacing_between_windings

    @property
    def len_y(self):
        return (self.spacing_between_windings + 2 * self.winding_radius) * self.number_of_windings_y + self.spacing_between_windings

    @property
    def total_area(self):
        return self.len_x * self.len_y

    @property
    def area_winding(self):
        return math.pi * self.winding_radius ** 2 - math.pi * self.inner_radius ** 2

    @property
    def area_cooling(self):
        return math.pi * self.inner_radius ** 2

    def draw_coil(self):
        fig, ax = plt.subplots(figsize=(8, 6))

        # Define parameters
        num_windings = int(self.number_of_windings_x * self.number_of_windings_y)
        wire_spacing = 2 * self.winding_radius+ self.spacing_between_windings  # Spacing between circles and rows

        # Plot coil
        for i in range(num_windings):
            # Calculate row and column index
            row = i // self.number_of_windings_x
            col = i % self.number_of_windings_x

            # Calculate x and y coordinates
            x = self.winding_radius + col * wire_spacing
            y = self.winding_radius + row * wire_spacing

            # Plot outer circle (blue)
            outer_circle = plt.Circle((x, y), self.winding_radius, color='blue', fill=False, linestyle='--')
            ax.add_patch(outer_circle)

            # Plot inner circle (red)
            inner_circle = plt.Circle((x, y), self.inner_radius, color='red', fill=False, linestyle='--')
            ax.add_patch(inner_circle)

            # Add self.winding_radius labels to the first circle
            if i == 0:
                ax.text(x + 0.1 * self.inner_radius - self.winding_radius, y + 0.4 * self.winding_radius, 'winding_radius', fontsize=12, verticalalignment='center')
                ax.plot([x - self.winding_radius, x], [y, y], color='black', linewidth=1)
                ax.text(x + 0.1 * self.inner_radius, y + self.winding_radius + 0.1 * self.inner_radius, 'spacing_between_windings', fontsize=12, verticalalignment='center')
                ax.plot([x, x], [y + self.inner_radius, y + self.inner_radius + self.spacing_between_windings], color='black', linewidth=1)
            if i == self.number_of_windings_x:
                ax.text(x - self.inner_radius*1.1, y + 0.4*self.inner_radius, 'inner_radius', fontsize=12, verticalalignment='center')
                ax.plot([x - self.inner_radius, x], [y, y], color='black', linewidth=1)
                

        # Draw box around coils
        box = Rectangle((-self.spacing_between_windings, - self.spacing_between_windings), self.len_x, self.len_y, edgecolor='black', linewidth=1, fill=False)
        ax.text(-self.spacing_between_windings - 2 * self.inner_radius, self.len_y/2-self.spacing_between_windings, 'len_y', fontsize=12, verticalalignment='center')
        ax.text(self.len_x/2 - self.spacing_between_windings - 0.4 * self.inner_radius, self.len_y + 0.2 * self.inner_radius, 'len_x', fontsize=12, verticalalignment='center')
        ax.add_patch(box)

        # Display important variables
        important_variables = {'winding_adius': self.winding_radius, 'inner_radius': self.inner_radius, 'spacing_between_windings': self.spacing_between_windings, 'length_x': wire_spacing*self.number_of_windings_x-self.spacing_between_windings, 'length_y': wire_spacing*self.number_of_windings_y-self.spacing_between_windings}
        text = '\n'.join([f'{key}: {value}' for key, value in important_variables.items()])
        ax.text(self.len_x + self.winding_radius * 2, self.len_y / 2 - self.spacing_between_windings, text, fontsize=12, verticalalignment='center')

        # Set aspect ratio to equal and adjust plot limits
        ax.set_aspect('equal', adjustable='box')
        ax.set_xlim(-self.winding_radius * 2, self.len_x + self.winding_radius * 2)
        ax.set_ylim(-self.winding_radius * 2, self.len_y + self.winding_radius * 2)
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_title('Coil with {} Windings of Bremsleitungen'.format(num_windings))
        ax.axis('off')  # Turn off axes
        plt.savefig(f"crosssections/{self.inner_radius}x{self.winding_radius}_crosssection")

class rechteckig(coil_geometry):
    def __init__(self, name, winding_width, winding_height, cooling_width, cooling_height, number_of_windings_x, number_of_windings_y, spacing_between_windings):
        super().__init__(name)
        self.winding_width = winding_width
        self.winding_height = winding_height
        self.cooling_width = cooling_width
        self.cooling_height = cooling_height
        self.spacing_between_windings = spacing_between_windings
        self.number_of_windings_x = number_of_windings_x
        self.number_of_windings_y = number_of_windings_y
        self.number_of_windings_total = number_of_windings_x * number_of_windings_y
        self.area_winding = self.winding_width * self.winding_height
        self.len_x = (spacing_between_windings + self.winding_width) * self.number_of_windings_x + self.spacing_between_windings
        self.len_y = (spacing_between_windings + self.winding_height) * self.number_of_windings_y + self.spacing_between_windings
        self.total_area = self.len_x * self.len_y
    
    def get_area_winding(self):
        return self.winding_width * self.winding_height - self.cooling_width * self.cooling_height

    def draw_coil(self):
        fig, ax = plt.subplots(figsize=(8, 6))

        # Define parameters
        num_windings = self.number_of_windings_x * self.number_of_windings_y
        wire_spacing_x = self.winding_width + self.spacing_between_windings  # Spacing between rectangles horizontally
        wire_spacing_y = self.winding_height + self.spacing_between_windings  # Spacing between rectangles vertically

        # Plot coil
        for i in range(num_windings):
            # Calculate row and column index
            row = i // self.number_of_windings_x
            col = i % self.number_of_windings_x

            # Calculate x and y coordinates
            x = col * wire_spacing_x
            y = row * wire_spacing_y

            # Plot outer rectangle (blue)
            outer_rectangle = Rectangle((x, y), self.winding_width, self.winding_height, edgecolor='blue', fill=False, linestyle='--')
            ax.add_patch(outer_rectangle)

            # Plot inner rectangle (red)
            inner_rectangle = Rectangle((x + (self.winding_width - self.cooling_width) / 2, y + (self.winding_height - self.cooling_height) / 2), self.cooling_width, self.cooling_height, edgecolor='red', fill=False, linestyle='--')
            ax.add_patch(inner_rectangle)

            # Add labels to the first rectangle
            if i == 1:
                ax.text(x, y - 0.5 * self.spacing_between_windings, 'winding_width', fontsize=12, verticalalignment='center')
                ax.plot([x, x + self.winding_width], [y, y], color='black', linewidth=1)
            elif i == 0:
                ax.text(x - 0.4 * self.spacing_between_windings, y + self.winding_height / 2, 'winding_height', fontsize=12, verticalalignment='center', horizontalalignment='center', rotation=90)
                ax.plot([x, x], [y, y + self.winding_height], color='black', linewidth=1)
            elif i == self.number_of_windings_x:
                ax.text(x + self.winding_width / 2, y + self.winding_height + 0.6 * self.spacing_between_windings, 'spacing_between_windings', fontsize=12, verticalalignment='center')
                ax.plot([x + self.winding_width / 2, x + self.winding_width / 2], [y + self.winding_height, y + self.winding_height + self.spacing_between_windings], color='black', linewidth=1)
            elif i == self.number_of_windings_x:
                ax.text(x + self.winding_width / 2, y - 0.4 * self.spacing_between_windings, 'cooling_height', fontsize=12, verticalalignment='center', horizontalalignment='center', rotation=90)
                ax.plot([x + (self.winding_width-self.cooling_width)/2, x + (self.winding_width-self.cooling_width)/2], [y + (self.winding_height-self.cooling_height)/2, y + winding_height + (winding_height-cooling_height)/2], color='black', linewidth=1)
            elif i == self.number_of_windings_x + 1:
                ax.text(x + self.winding_width / 2, y - 0.4 * self.spacing_between_windings, 'cooling_width', fontsize=12, verticalalignment='center', horizontalalignment='center')
                ax.plot([x + (self.winding_width-self.cooling_width)/2, x + self.cooling_width + (self.winding_width-self.cooling_width)/2], [y + (self.winding_height-self.cooling_height)/2, y+ (self.winding_height-self.cooling_height)/2], color='black', linewidth=1)

        # Draw box around coils
        box = Rectangle((-self.spacing_between_windings, -self.spacing_between_windings), self.len_x, self.len_y, edgecolor='black', linewidth=1, fill=False)
        ax.text(-self.spacing_between_windings - self.len_x * 0.2, self.len_y / 2, 'len_y', fontsize=12, verticalalignment='center')
        ax.text(self.len_x / 2 - self.len_x * 0.01, self.len_y + self.len_x * 0.01, 'len_x', fontsize=12, verticalalignment='center', horizontalalignment='center')
        ax.add_patch(box)

        # Display important variables
        important_variables = {
            'winding_width': self.winding_width,
            'winding_height': self.winding_height,
            'cooling_width': self.cooling_width,
            'cooling_height': self.cooling_height,
            'spacing_between_windings': self.spacing_between_windings,
            'length_x': self.len_x,
            'length_y': self.len_y
        }
        text = '\n'.join([f'{key}: {value}' for key, value in important_variables.items()])
        ax.text(self.len_x + self.winding_width, self.len_y / 2, text, fontsize=12, verticalalignment='center')

        # Set aspect ratio to equal and adjust plot limits
        ax.set_aspect('equal', adjustable='box')
        ax.set_xlim(-self.spacing_between_windings, self.len_x + self.winding_width)
        ax.set_ylim(-self.spacing_between_windings, self.len_y + self.winding_height)
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_title('Coil with {} Windings'.format(num_windings))
        ax.axis('off')  # Turn off axes
        plt.show()
