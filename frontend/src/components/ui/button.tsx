import * as React from 'react'
import { Slot } from '@radix-ui/react-slot'
import { cva, type VariantProps } from 'class-variance-authority'
import { cn } from '../../lib/utils'

const buttonVariants = cva('ui-button', {
  variants: {
    variant: {
      default: 'ui-button-default',
      secondary: 'ui-button-secondary',
      outline: 'ui-button-outline',
      ghost: 'ui-button-ghost',
      destructive: 'ui-button-destructive',
      link: 'ui-button-link',
    },
    size: {
      default: 'ui-button-md',
      sm: 'ui-button-sm',
      lg: 'ui-button-lg',
      icon: 'ui-button-icon',
    },
  },
  defaultVariants: { variant: 'default', size: 'default' },
})

export interface ButtonProps extends React.ButtonHTMLAttributes<HTMLButtonElement>, VariantProps<typeof buttonVariants> {
  asChild?: boolean
}

export function Button({ className, variant, size, asChild = false, ...props }: ButtonProps) {
  const Component = asChild ? Slot : 'button'
  return <Component className={cn(buttonVariants({ variant, size }), className)} {...props} />
}
