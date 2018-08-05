import { isArray } from 'lodash';

export function noop(ret: any) { if (ret !== undefined) { return ret; } }

export type EmptyObject = {};

export interface Dictionary<S> {
    [id: string]: S;
}

export function arrayToDictionary<T, S>(array: T[], getName: (v: T) => string, getValue: (v: T) => S): Dictionary<S> {
    return array.reduce((result, a) => {
        result[getName(a)] = getValue(a);
        return result;
    }, {});
}

// lodash merge of 2 arrays merges the keys:
// _.merge({ a: [1, 2] }, { a: [3] })) // { a: [3, 2] }
// this mergeWith customizer forces arrays to be replaced:
// _.mergeWith({ a: [1, 2] }, { a: [3] }, { a: [3] }, arrayReplacementCustomizer)) // { a: [3] };
export function arrayReplacementCustomizer(obj: any[], src: any[]) {
    if (isArray(obj)) {
        return src;
    }
}