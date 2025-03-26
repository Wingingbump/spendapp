declare module 'react-icons/fi' {
  import { ComponentType, SVGAttributes } from 'react';

  interface IconProps extends SVGAttributes<SVGElement> {
    size?: string | number;
  }

  export const FiSearch: ComponentType<IconProps>;
  export const FiBell: ComponentType<IconProps>;
  export const FiUser: ComponentType<IconProps>;
  export const FiGrid: ComponentType<IconProps>;
  export const FiPieChart: ComponentType<IconProps>;
  export const FiDollarSign: ComponentType<IconProps>;
  export const FiTrendingUp: ComponentType<IconProps>;
  export const FiFileText: ComponentType<IconProps>;
  export const FiSettings: ComponentType<IconProps>;
  export const FiHelpCircle: ComponentType<IconProps>;
  export const FiLogOut: ComponentType<IconProps>;
  export const FiCreditCard: ComponentType<IconProps>;
} 