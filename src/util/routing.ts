import { RouteComponentProps } from 'react-router';

import { EmptyObject } from './base';

export type RouteAwareComponentProps<T, S> = T & RouteComponentProps<S>;

export type EmptyRouteAwareComponentProps<T> = RouteAwareComponentProps<T, EmptyObject>;