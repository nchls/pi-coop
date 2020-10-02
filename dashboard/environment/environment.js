import React from 'react';
import { getDay, getUnixTime, fromUnixTime, parseISO } from 'date-fns';
import { XYPlot, XAxis, YAxis, HorizontalGridLines, VerticalGridLines, LineSeries } from 'react-vis';
import { atom, useRecoilValue } from 'recoil';

import { useAPIPoll } from '../app/utils';
import './environment.scss';


const weekdays = [
	'Sun',
	'Mon',
	'Tue',
	'Wed',
	'Thu',
	'Fri',
	'Sat'
];

export const environmentState = atom({
	key: 'environment',
	default: {
		fetched: false,
		loggingEnabled: undefined,
		logEntries: {
			temperature: [],
			pressure: [],
			humidity: [],
			gas: [],
		}
	}
});

const Environment = () => {
	useAPIPoll(environmentState, '/environment/logs', 60000 * 10);
	const environment = useRecoilValue(environmentState);

	const [earliestTimes, latestValues] = ['temperature', 'pressure', 'humidity', 'gas'].reduce((accumulator, property) => {
		if (environment.logEntries[property].length === 0) {
			accumulator[0][property] = undefined;
			accumulator[1][property] = undefined;
		} else {
			accumulator[0][property] = environment.logEntries[property][0][0];
			let val = environment.logEntries[property][environment.logEntries[property].length - 1][1];
			if (property === 'gas') {
				val /= 1000;
			}
			accumulator[1][property] = val;
		}
		return accumulator;
	}, [{}, {}]);

	const chartData = {};
	const firstInDay = {
		'temperature': [],
		'pressure': [],
		'humidity': [],
		'gas': [],
	};
	['temperature', 'pressure', 'humidity', 'gas'].forEach((property) => {
		const entries = environment.logEntries[property];
		let previousDay = getDay(parseISO(earliestTimes[property]));
		chartData[property] = entries.map((entry) => {
			const dt = parseISO(entry[0]);
			const ts = getUnixTime(dt);
			if (getDay(dt) !== previousDay) {
				firstInDay[property].push(ts);
				previousDay = getDay(dt);
			}
			let val = entry[1];
			if (property === 'gas') {
				val /= 1000;
			}
			return {
				x: ts,
				y: val
			};
		});
	});

	return (
		<>
			<div className="panel-heading">Coop Environment</div>
			<div className="panel-block temperature">
				<div>
					Temperature: { latestValues.temperature }°F
				</div>
				<XYPlot width={300} height={300} yDomain={[-10, 120]}>
					<HorizontalGridLines />
					<VerticalGridLines tickValues={firstInDay.temperature} />
					<LineSeries data={chartData.temperature} />
					<XAxis tickFormat={v => weekdays[getDay(fromUnixTime(v))]} tickValues={firstInDay.temperature} />
					<YAxis />
				</XYPlot>
			</div>
			<div className="panel-block pressure">
				<div>
					Pressure: { latestValues.pressure } mb
				</div>
				<XYPlot width={300} height={300} yDomain={[970, 1040]}>
					<HorizontalGridLines />
					<VerticalGridLines tickValues={firstInDay.pressure} />
					<LineSeries data={chartData.pressure} />
					<XAxis tickFormat={v => weekdays[getDay(fromUnixTime(v))]} tickValues={firstInDay.pressure} />
					<YAxis />
				</XYPlot>
			</div>
			<div className="panel-block humidity">
				<div>
					Humidity: { latestValues.humidity }%
				</div>
				<XYPlot width={300} height={300} yDomain={[0, 100]}>
					<HorizontalGridLines />
					<VerticalGridLines tickValues={firstInDay.humidity} />
					<LineSeries data={chartData.humidity} />
					<XAxis tickFormat={v => weekdays[getDay(fromUnixTime(v))]} tickValues={firstInDay.humidity} />
					<YAxis />
				</XYPlot>
			</div>
			<div className="panel-block gas">
				<div>
					Gas: { latestValues.gas } kOhms
				</div>
				<XYPlot width={300} height={300} yDomain={[0, 200]}>
					<HorizontalGridLines />
					<VerticalGridLines tickValues={firstInDay.gas} />
					<LineSeries data={chartData.gas} />
					<XAxis tickFormat={v => weekdays[getDay(fromUnixTime(v))]} tickValues={firstInDay.gas} />
					<YAxis />
				</XYPlot>
			</div>
		</>
	);
};

export default Environment;
